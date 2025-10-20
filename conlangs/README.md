# Drafting Languages from Drafts: Building a Functional Constructed Language Translator with Cycle-Consistent Fine-Tuning

## Abstract

We present a training recipe for building a fully functional machine translator for a constructed language (conlang) from a *small draft corpus* of approximate bilingual examples. The approach blends (i) **bidirectional supervised fine-tuning (SFT)** on a single model with direction tags and (ii) **cycle-consistent reinforcement-style fine-tuning** that optimizes a **round-trip objective**. The core signal encourages the model (T) to produce translations whose **back-translation** $(T^{-1}(T(s)))$ closely matches the source sentence (s), while light regularizers curb trivial identity mappings and length drift. A **phrase bank** supplies diverse prompts for round-trip training, decoupling SFT pairs from the self-supervised signal. We detail the method, provide a practical algorithm and data specification, propose evaluation protocols that measure both semantic fidelity and language-internal consistency, and outline ablations and limitations. The recipe targets rapid bootstrapping of a usable conlang translator while the conlang’s grammar is still evolving.

---

## 1. Introduction

Creating a new naturalistic language typically demands years of design plus large, curated corpora before high-quality translation becomes feasible. Large language models (LLMs) change this workflow: with a modest set of **draft bilingual examples** that sketch orthography, morphology, and syntax, one can train a translator that *fills in the gaps* by relying on model priors and a powerful **round-trip training signal**.

This paper describes a principled and practical path to such a system:

1. **Single bidirectional model.** One set of parameters handles both directions via explicit direction tags. Shared parameters concentrate knowledge into a **single latent space**, encouraging coherent mappings across directions.

2. **Cycle-consistent objective.** The system improves by **minimizing information loss** in round-trip translation: for a source sentence (s), translate forward (y=T(s)) and back-translate $(\hat{s}=T^{-1}(y))$, then reward high agreement between (s) and $(\hat{s})$.

3. **Small supervised seed; large self-supervised loop.** A small supervised seed aligns the mapping; a round-trip objective scales quality using a **phrase bank** that can be far larger and unpaired.

This recipe yields a translator that converges quickly, stays faithful to the conlang’s design constraints, and adapts smoothly as the conlang specification evolves.

---

## 2. Background and Motivation

**Draft corpora** for newly designed languages rarely cover the full space of constructions. Purely supervised learning tends to mirror the drafts’ gaps. In contrast, **round-trip (cycle) objectives** supply an abundant training signal: every sentence can become a training example without a human target. When unified in a single bidirectional model, forward and backward directions share structure and promote mutual consistency.

Two practical questions guide the design:

* **How do we prevent trivial solutions?** A cycle loss alone can make the system favor near-identity outputs. Lightweight regularizers address this by mildly penalizing lexical overlap with the source and constraining length ratios.

* **How do we scale beyond the draft pairs?** A **phrase bank**—monolingual sentences, templated examples, or harvested public sentences—feeds the round-trip loop and broadens coverage without additional human annotation.

---

## 3. Problem Setup

Let (L_s) be a high-resource source language and (L_c) the constructed target language. We train a single model $(T_\theta(x,|,d))$ that maps input text (x) to the other language, controlled by a **direction tag** $(d \in {\text{S2C}, \text{C2S}})$.

We assume:

* A **draft parallel set** $(\mathcal{D}_{\text{draft}}={(u_i,v_i)})$ with approximate translations in both directions (hundreds to a few thousand pairs).
* A **phrase bank** $(\mathcal{B}={b_j})$ consisting of sentences in the base language (the larger the bank the better).

**Goal.** Produce a translator that (i) preserves source meaning across directions, (ii) respects conlang constraints (orthography, morphology), and (iii) generalizes beyond the drafts.

---

## 4. Method

### 4.1 Single-Model Bidirectional SFT

We first perform supervised fine-tuning on $(\mathcal{D}_{\text{draft}})$ using chat-style examples with explicit tags:

```
<System> Olivolingvo is a derivative of Esperanto focused on the Mediterranean. It largely strips out the non-Mediterranean components replacing them with grammar and vocabulary from Hebrew, ancient Egyptian, and Tamazight. Translate between the two languages; obey the direction tag.
<User> <S2C>
<User> [source sentence in L_s]
<Assistant> [target sentence in L_c]
```

and symmetrically for $( \text{C2S} )$. Balancing directions encourages a shared latent space and stable inverse behavior.

### 4.2 Cycle-Consistent Round-Trip Objective

We continue from the SFT checkpoint with **reinforcement-style fine-tuning** that optimizes a scalar reward for each input sentence $(s\in\mathcal{B})$.

**Forward step.** $(y=T_\theta(s,|,\text{S2C}))$

**Backward step.** $(\hat{s}=T_\theta(y,|,\text{C2S}))$

**Reward.** We use a **likelihood-based round-trip signal** plus light regularizers:
$[
r(s) ;=; \underbrace{\frac{1}{|\hat{s}|}\sum_{t=1}^{|\hat{s}|}\log p_\theta!\left(\hat{s}*t ,\middle|, \hat{s}*{<t}, , y, , \text{C2S}\right)}_{\text{mean token logprob } \approx -\text{CE}(s,\hat{s})}
;-; \beta,\text{Overlap}(s,y)
;-; \gamma,\text{LenDrift}(s,y).
]$

* The first term maximizes the model’s probability of regenerating the source after a round trip (a length-normalized negative cross-entropy).
* $(\text{Overlap})$ computes Jaccard similarity over words or character (n)-grams to **discourage identity mapping**.
* $(\text{LenDrift}(s,y)=\big|\frac{|y|}{|s|}-1\big|)$ keeps translations length-stable without forcing strict equality.

The same recipe handles inputs that originate in (L_c) by flipping the direction tags.

### 4.3 Phrase Bank Sampling

A large phrase bank offers diversity and better coverage. Two practical regimes:

* **Sampling:** choose a fresh subset $((5\text{k})–(50\text{k}) lines)$ per training job with a new seed; this improves exploration and reduces overfitting.
* **Full sweep:** use the entire bank when the bank is modest and compute is ample.

### 4.4 Constraints and Validators

Lightweight validators strengthen language-internal coherence:

* **Orthography and character whitelist.**
* **Morphological pattern checks** (e.g., suffix inventories, affix order).
* **Forbidden sequences** (e.g., illegal clusters).
* **Optional structured-output checks** (e.g., JSON fields for gloss or notes).

Validators can contribute additional small penalties or serve as post-hoc quality filters.

### 4.5 Training Algorithm

**Stage A: SFT.**

1. Format $(\mathcal{D}_{\text{draft}})$ into bidirectional chat examples.
2. Fine-tune the base model for a few epochs.

**Stage B: Cycle-Consistent Fine-Tuning.**

1. Sample a subset from $(\mathcal{B})$.
2. For each sentence (s): produce $(y=T_\theta(s,|,\text{S2C}))$, back-translate $(\hat{s}=T_\theta(y,|,\text{C2S}))$, compute (r(s)), and update (\theta) to maximize (r).
3. Rotate seeds and subsets across runs for breadth.

---

## 5. Practical Implementation

### 5.1 Data Specifications

* **Draft pairs.** Mixed directions; concise sentences that cover morphology and syntax “corner cases” (comparatives, negation scope, relative clauses, numerals, tense/aspect/mood).
* **Phrase bank.** Clean sentences from varied domains; optionally include templated constructions to exercise grammar.

### 5.2 Hyperparameters (sensible defaults)

* **SFT.** 2–4 epochs; batch size auto; learning-rate multiplier ≈ 1.0; temperature low at inference (0–0.3).
* **Cycle stage.** 2–4 epochs over the sampled subset; reward weights (\beta\in[0.05,0.10]), (\gamma\in[0.03,0.07]); back-translation at temperature 0 for stable log-prob scoring.

### 5.3 Guarding Against Degenerate Behaviors

* **Identity bias:** handled by the overlap penalty and by inspecting top-k overlap statistics.
* **Length collapse or sprawl:** managed by the length-drift penalty.
* **Vocabulary leakage from (L_s):** optional soft penalties for disallowed characters or n-grams.

---

## 6. Evaluation

### 6.1 Round-Trip Metrics

Evaluate on a held-out set of source-language sentences:

* **RTT-chrF / RTT-BLEU / RTT-BERTScore** between (s) and (\hat{s}).
* **Mean token log-prob** of back-translation.

These metrics correlate with meaning preservation across the cycle.

### 6.2 Conlang Fidelity

* **Validator pass rate:** proportion of outputs that satisfy orthographic and morphological constraints.
* **Distributional checks:** bigram or syllable statistics compared with seed examples.
* **Affix productivity grid:** coverage of derivational and inflectional patterns.

### 6.3 Human Evaluation

* **Adequacy:** preservation of meaning.
* **Fluency (target side):** well-formedness according to the conlang’s rules.
* **Consistency across paraphrases:** stable mapping for semantically equivalent inputs.

---

## 7. Ablation Studies

* **Single vs. dual model.** A single bidirectional model typically yields stronger cycle consistency and smaller footprint.
* **Effect of overlap penalty (\beta).** Track identity rate, overlap distribution, and RTT metrics while sweeping (\beta).
* **Phrase bank size and sampling.** Measure gains from 5k → 50k → full-bank regimes; resample seeds to quantify variance.
* **Validator integration.** Add/remove validator-based penalties to observe shifts in fidelity vs. fluency.

---

## 8. Limitations and Risks

* **Style over-regularization.** Strong penalties can oversmooth target style; gentle weights help maintain expressiveness.
* **Draft biases.** The drafts define the initial grammar; unexpected artifacts in drafts tend to persist until counter-examples appear in the phrase bank or additional curated pairs.
* **Safety and content constraints.** The phrase bank can include sensitive topics; moderation and filtering pipelines maintain responsible behavior.

---

## 9. Reproducibility Checklist

* Release the **draft pairs** and **phrase bank** (or generators), including the direction-tagging scheme.
* Report **hyperparameters**, **reward weights**, and **sampling seeds**.
* Provide **training logs** of reward curves and evaluation metrics.
* Include **validator definitions** (regexes, whitelists, morphology checks).
* Share **pseudo-code** and a minimal **grader function**.

---

## 10. Pseudo-Code

### 10.1 Cycle-Consistent Fine-Tuning Loop

```python
for epoch in range(E):
    subset = sample_from_phrase_bank(B, size=S, seed=seed+epoch)
    for s in subset:
        # forward: source -> conlang
        y = model.generate(tag="S2C", input=s, temperature=0.2)

        # backward: conlang -> source with logprobs for reward
        bt, logprobs = model.generate_with_logprobs(tag="C2S", input=y, temperature=0)

        mean_lp = mean(logprobs)
        overlap = jaccard(s, y)               # identity deterrent
        drift   = abs(len(y)/max(1,len(s)) - 1)

        reward = ALPHA*mean_lp - BETA*overlap - GAMMA*drift
        model.update(reward)                   # reinforcement-style fine-tuning step
```

### 10.2 Validator Sketch

```python
def validator(text):
    score = 0
    if not CHAR_WHITELIST.fullmatch(text): score += 1
    for rx in FORBIDDEN: 
        if rx.search(text): score += 1
    return score  # 0 means clean
```

---

## 11. Conclusion

A small set of approximate bilingual drafts, coupled with a **single bidirectional model** and a **cycle-consistent objective**, yields a practical path to a functional conlang translator. The approach learns from limited supervision and scales via self-supervision over a large phrase bank. Lightweight validators steer the system toward internal coherence, while round-trip metrics and human judgements capture quality measured in use. This recipe supports rapid iteration as the conlang evolves, enabling creators to move from sketches to a working translator with modest resources.

---

## Appendix A. Data Templates

**Bidirectional SFT (chat JSONL)**

```json
{"messages":[
  {"role":"system","content":"Olivolingvo is a derivative of Esperanto focused on the Mediterranean. It largely strips out the non-Mediterranean components replacing them with grammar and vocabulary from Hebrew, ancient Egyptian, and Tamazight. Translate between the two languages; obey the direction tag."},
  {"role":"user","content":"<S2C>\n[source sentence]"},
  {"role":"assistant","content":"[target sentence]"}
]}
{"messages":[
  {"role":"system","content":"Olivolingvo is a derivative of Esperanto focused on the Mediterranean. It largely strips out the non-Mediterranean components replacing them with grammar and vocabulary from Hebrew, ancient Egyptian, and Tamazight. Translate between the two languages; obey the direction tag."},
  {"role":"user","content":"<C2S>\n[target sentence]"},
  {"role":"assistant","content":"[source sentence]"}
]}
```

**Phrase Bank to RFT Pool (chat JSONL)**

```json
{"src":"[sentence in source]","dir":"S2C","messages":[
  {"role":"system","content":"Olivolingvo is a derivative of Esperanto focused on the Mediterranean. It largely strips out the non-Mediterranean components replacing them with grammar and vocabulary from Hebrew, ancient Egyptian, and Tamazight. Translate between the two languages; obey the direction tag."},
  {"role":"user","content":"<S2C>\n[sentence in source]"}
]}
{"src":"[sentence in conlang]","dir":"C2S","messages":[
  {"role":"system","content":"Olivolingvo is a derivative of Esperanto focused on the Mediterranean. It largely strips out the non-Mediterranean components replacing them with grammar and vocabulary from Hebrew, ancient Egyptian, and Tamazight. Translate between the two languages; obey the direction tag."},
  {"role":"user","content":"<C2S>\n[sentence in conlang]"}
]}
```

---

## Appendix B. Suggested Metrics

* **Round-Trip:** RTT-chrF, RTT-BLEU, RTT-BERTScore, mean token log-prob.
* **Fidelity:** validator pass rate; distributional similarity; affix productivity coverage.
* **Human:** adequacy (0–5), fluency (0–5), and consistency assessments over paraphrase sets.

---

*This paper focuses on a general method for conlang translation from limited drafts by optimizing a round-trip objective with a single bidirectional model, supported by lightweight validators and scalable phrase-bank sampling.*
