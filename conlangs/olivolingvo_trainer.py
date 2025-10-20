# train_olivolingvo.py
# End-to-end: SFT bidirectional EO↔Olivolingvo translator + RFT with round-trip objective
# Requires: pip install openai requests
# Env: export OPENAI_API_KEY=sk-...

import os, re, json, time, random, inspect, requests
from typing import List
from openai import OpenAI

# ==========================
# Config
# ==========================
# 1) Prototype bilingual data (chat JSONL with both directions)
PROTOTYPE_FILE = "olivolingvo_prototype.jsonl"

# 2) Phrase bank (plain text or JSONL). Each line either:
#    - Plain text (assumed Esperanto)
#    - Or JSON like {"text": "...", "lang": "eo"} or {"text": "...", "lang": "olv"}
PHRASE_BANK_FILE = "phrase_bank.txt"

# 3) Where to materialize the sampled RFT dataset
RFT_SAMPLES_FILE = "rft_phrase_pool.jsonl"

# Base for initial SFT
BASE_MODEL = "gpt-4o-mini-2024-08-06"

# Direction tags
EO2OLV = "<EO2OLV>"
OLV2EO = "<OLV2EO>"

# RFT sampling strategy
USE_FULL_PHRASE_BANK = False       # True = use entire bank; False = random sample below
RFT_SAMPLE_SIZE = 10000            # number of phrases to draw when sampling
SHUFFLE_SEED = 42                  # change per run to rotate coverage

# Reward weights
ALPHA = 1.0   # reward for mean token logprob of back-translation (≈ -CE)
BETA  = 0.08  # overlap penalty to deter identity mapping
GAMMA = 0.05  # length drift penalty

# Instantiate client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ==========================
# Utilities
# ==========================
def jaccard_overlap(a: str, b: str) -> float:
    A = set(re.findall(r"\w+", a.lower()))
    B = set(re.findall(r"\w+", b.lower()))
    return 0.0 if not A or not B else len(A & B) / len(A | B)

def length_drift(a: str, b: str) -> float:
    return 0.0 if len(a) == 0 else abs(len(b) / len(a) - 1.0)

def upload_file(path: str, purpose="fine-tune") -> str:
    with open(path, "rb") as f:
        r = requests.post(
            "https://api.openai.com/v1/files",
            headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
            files={"file": f},
            data={"purpose": purpose},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["id"]

# ==========================
# Build RFT training pool from phrase bank
# ==========================
def load_phrase_bank(path: str):
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            if raw.startswith("{"):
                try:
                    obj = json.loads(raw)
                    text = obj.get("text") or obj.get("src") or obj.get("sentence")
                    lang = obj.get("lang", "eo").lower()
                    if text:
                        lines.append((text, lang))
                except Exception:
                    # treat as plain text on parse hiccup
                    lines.append((raw, "eo"))
            else:
                lines.append((raw, "eo"))
    return lines

def build_rft_pool(phrase_bank_path: str, out_path: str, use_full: bool, sample_size: int, seed: int = 42):
    pool = load_phrase_bank(phrase_bank_path)
    if not pool:
        raise RuntimeError("Phrase bank is empty.")

    rng = random.Random(seed)
    if use_full or sample_size >= len(pool):
        chosen = pool[:]  # full bank
        rng.shuffle(chosen)
    else:
        chosen = rng.sample(pool, sample_size)

    # Create chat JSONL where each line is a prompt for forward translation
    # We also include 'src' and 'dir' for the grader.
    with open(out_path, "w", encoding="utf-8") as w:
        for text, lang in chosen:
            if lang == "olv":
                # Olivolingvo -> EO direction
                msg = f"{OLV2EO}\n{text}"
                direction = "OLV2EO"
            else:
                # Esperanto -> Olivolingvo direction (default)
                msg = f"{EO2OLV}\n{text}"
                direction = "EO2OLV"

            record = {
                "src": text,
                "dir": direction,
                "messages": [
                    {"role": "system", "content": "Translate between Esperanto and Olivolingvo per the direction tag."},
                    {"role": "user",   "content": msg}
                ]
            }
            w.write(json.dumps(record, ensure_ascii=False) + "\n")

    return out_path, len(chosen)

# ==========================
# Grader for RFT (cycle consistency)
# ==========================
def grade(sample, item=None):
    """
    Reward = mean_logprob(back-translation) - BETA*overlap(s,y) - GAMMA*length_drift(s,y)
    - sample["output_text"] is the model's forward output y for messages in the sample.
    - item["src"] provides the original source sentence s.
    - item["dir"] gives the direction we used for the forward call.
    """
    import os, re
    from openai import OpenAI

    client = OpenAI()

    y = (sample.get("output_text") or "").strip()
    s = ""
    direction = ""
    if isinstance(item, dict):
        s = item.get("src", "")
        direction = item.get("dir", "EO2OLV")

    # Decide back-translation direction by flipping the forward tag
    EO2OLV = os.getenv("EO2OLV", "<EO2OLV>")
    OLV2EO = os.getenv("OLV2EO", "<OLV2EO>")
    BT_MODEL = os.getenv("BACKTRANSLATOR_MODEL") or os.getenv("TRANSLATOR_MODEL") or "ft:olivolingvo-translator-sft"

    if direction == "EO2OLV":
        # back: OLV -> EO
        back_tag = OLV2EO
    else:
        # back: EO -> OLV
        back_tag = EO2OLV

    # 1) Back-translate with token logprobs
    resp = client.chat.completions.create(
        model=BT_MODEL,
        messages=[
            {"role": "system", "content": "Translate between Esperanto and Olivolingvo per the direction tag."},
            {"role": "user",   "content": f"{back_tag}\n{y}"}
        ],
        temperature=0,
        max_output_tokens=512,
        logprobs=True,
        top_logprobs=0
    )
    bt = resp.choices[0].message.content or ""
    token_logprobs = []
    lp_block = getattr(resp.choices[0], "logprobs", None)
    if lp_block and getattr(lp_block, "content", None):
        token_logprobs = [t.logprob for t in lp_block.content]
    mean_lp = (sum(token_logprobs) / max(1, len(token_logprobs))) if token_logprobs else -10.0

    # 2) Anti-degeneration terms on forward step (s vs y)
    def _jaccard_overlap(a: str, b: str) -> float:
        A = set(re.findall(r"\w+", a.lower()))
        B = set(re.findall(r"\w+", b.lower()))
        return 0.0 if not A or not B else len(A & B) / len(A | B)

    def _length_drift(a: str, b: str) -> float:
        return 0.0 if len(a) == 0 else abs(len(b) / len(a) - 1.0)

    copy = _jaccard_overlap(s, y)
    drift = _length_drift(s, y)

    ALPHA = float(os.getenv("ALPHA", "1.0"))
    BETA  = float(os.getenv("BETA",  "0.08"))
    GAMMA = float(os.getenv("GAMMA", "0.05"))

    score = float(ALPHA * mean_lp - BETA * copy - GAMMA * drift)
    return {
        "steps": [{
            "description": "Back-translation mean logprob with overlap/length penalties.",
            "conclusion": f"mean_logprob={mean_lp:.4f}, copy={copy:.3f}, drift={drift:.3f}"
        }],
        "result": score
    }

# ==========================
# SFT: Train the initial translator
# ==========================
def run_sft():
    tf_id = upload_file(PROTOTYPE_FILE)
    job = client.fine_tuning.jobs.create(
        model=BASE_MODEL,
        training_file=tf_id,
        suffix="olivolingvo-translator-sft",
        hyperparameters={"n_epochs": 3, "batch_size": "auto", "learning_rate_multiplier": 1.0},
    )
    print("🚀 SFT job:", job.id)
    print("🔗", f"https://platform.openai.com/finetune/{job.id}")

    while True:
        status = client.fine_tuning.jobs.retrieve(job.id)
        if status.status in ("succeeded", "failed", "cancelled"):
            print("✅ SFT finished:", status.status)
            if status.status == "succeeded":
                print("🔧 Translator model:", status.fine_tuned_model)
                return status.fine_tuned_model
            raise RuntimeError(f"SFT ended with status={status.status}")
        time.sleep(30)

# ==========================
# RFT: Round-trip fine-tuning using phrase bank
# ==========================
def run_rft(translator_model: str):
    # 1) Build the RFT training pool from the phrase bank
    out_path, n = build_rft_pool(
        PHRASE_BANK_FILE,
        RFT_SAMPLES_FILE,
        use_full=USE_FULL_PHRASE_BANK,
        sample_size=RFT_SAMPLE_SIZE,
        seed=SHUFFLE_SEED
    )
    print(f"🧺 RFT pool: {out_path} ({n} samples)")

    # 2) Validate grader
    grader_src = inspect.getsource(grade)
    validate_payload = {"grader": {"type": "python", "source": grader_src}}
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}
    v = requests.post(
        "https://api.openai.com/v1/fine_tuning/alpha/graders/validate",
        json=validate_payload, headers=headers, timeout=60
    )
    v.raise_for_status()
    print("✅ Grader validated.")

    # 3) Upload the RFT pool
    rft_file_id = upload_file(out_path)

    # 4) Launch RFT — continue training FROM the SFT translator model
    job_body = dict(
        training_file=rft_file_id,
        model=translator_model,  # continue from the SFT checkpoint
        suffix="olivolingvo-translator-rft",
        method=dict(
            type="reinforcement",
            reinforcement=dict(
                grader=validate_payload["grader"],
                hyperparameters=dict(
                    n_epochs=3,
                    compute_multiplier=1.0,
                    reasoning_effort="low",
                ),
            ),
        ),
        seed=SHUFFLE_SEED,
        environment_variables={
            # grader runtime settings
            "TRANSLATOR_MODEL": translator_model,  # back-translation model
            "BACKTRANSLATOR_MODEL": translator_model,
            "EO2OLV": EO2OLV,
            "OLV2EO": OLV2EO,
            "ALPHA": str(ALPHA),
            "BETA": str(BETA),
            "GAMMA": str(GAMMA),
        },
    )
    r = requests.post("https://api.openai.com/v1/fine_tuning/jobs", json=job_body, headers=headers, timeout=60)
    r.raise_for_status()
    job = r.json()
    print("🚀 RFT job:", job["id"])
    print("🔗", "https://platform.openai.com/finetune/" + job["id"])
    return job["id"]

# ==========================
# Main
# ==========================
if __name__ == "__main__":
    print("=== Step 1: SFT — initial Olivolingvo translator ===")
    translator_model = run_sft()

    print("\n=== Step 2: RFT — round-trip training with phrase bank ===")
    run_rft(translator_model)
