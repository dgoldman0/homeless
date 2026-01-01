import os
import sqlite3
import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import discord
from discord.ext import commands, tasks

from openai import OpenAI

"""
Discord Hourly Digest Bot

Purpose
-------
Listens to a single Discord text channel, collects messages in fixed one-hour
UTC windows, and produces an hourly distilled summary using OpenAI. Each digest
is stored locally in SQLite for later retrieval or frontend use.

High-level Flow
---------------
1. Bot connects to Discord with message content intent enabled.
2. A background task aligns to the top of each UTC hour.
3. For the previous hour:
   - Fetches channel messages (excluding bot messages).
   - Normalizes them into a chronological transcript.
   - Trims transcript if it exceeds size limits.
4. Sends the transcript to OpenAI with a system instruction that:
   - Summarizes events
   - Analyzes themes, decisions, and disagreements
   - Extracts action items, open questions, and notable quotes
5. Stores the resulting digest in SQLite with time window metadata.
6. Optionally posts the digest back into the channel.
7. Provides a minimal command to fetch the most recent digest.

Design Notes
------------
- Uses sqlite3 for simple, zero-dependency persistence.
- Uses discord.py background tasks instead of cron or external schedulers.
- OpenAI calls are isolated and run in a thread to avoid blocking the event loop.
- All timestamps and windows are handled in UTC for consistency.
- Transcript size and message count are capped to control token usage.

Intended Evolution
------------------
- Replace or expand the system instruction as requirements mature.
- Add a frontend or API layer on top of the digest database.
- Support multiple channels, variable windows, or on-demand digests.
- Add richer metadata extraction (decisions, votes, sentiment, etc.).
"""

# ----------------------------
# Config
# ----------------------------

@dataclass(frozen=True)
class Config:
    discord_token: str
    channel_id: int
    openai_model: str
    db_path: str
    max_messages: int
    max_chars: int
    max_output_tokens: int
    post_digest_to_channel: bool


def load_config() -> Config:
    discord_token = os.getenv("DISCORD_TOKEN", "").strip()
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    channel_id_raw = os.getenv("CHANNEL_ID", "").strip()

    if not discord_token:
        raise RuntimeError("DISCORD_TOKEN is required")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    if not channel_id_raw.isdigit():
        raise RuntimeError("CHANNEL_ID is required and must be a number")

    # OpenAI SDK reads OPENAI_API_KEY from env automatically.
    os.environ["OPENAI_API_KEY"] = openai_api_key

    return Config(
        discord_token=discord_token,
        channel_id=int(channel_id_raw),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.2").strip() or "gpt-5.2",
        db_path=os.getenv("DB_PATH", "digests.db").strip() or "digests.db",
        max_messages=int(os.getenv("MAX_MESSAGES", "350")),     # cap history pulled per hour
        max_chars=int(os.getenv("MAX_CHARS", "80_000")),        # cap transcript size
        max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "900")),
        post_digest_to_channel=os.getenv("POST_DIGEST", "0").strip() == "1",
    )


CONFIG = load_config()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("digestbot")

openai_client = OpenAI()


# ----------------------------
# Prompt (revise later)
# ----------------------------

SYSTEM_INSTRUCTIONS = """You create an hourly digest for a Discord channel.

Goal:
- Distill what happened in the last hour with high signal and zero fabrication.

Output format (use headings exactly):
SUMMARY:
- bullets, 5–10 lines max

ANALYSIS:
- major themes
- decisions or conclusions
- disagreements or confusion points

ACTION ITEMS:
- bullet list; include owner if clear; include due date if mentioned

OPEN QUESTIONS:
- bullet list

NOTABLE QUOTES:
- 3–8 short bullets formatted as: "quote" — username

Style:
- concise, concrete, name entities, keep uncertainty explicit
"""


# ----------------------------
# SQLite helpers (digest storage)
# ----------------------------

def _db_init(db_path: str) -> None:
    con = sqlite3.connect(db_path)
    try:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS digests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER NOT NULL,
                window_start TEXT NOT NULL,
                window_end TEXT NOT NULL,
                message_count INTEGER NOT NULL,
                digest_text TEXT NOT NULL,
                openai_response_id TEXT,
                created_at TEXT NOT NULL,
                UNIQUE(channel_id, window_end)
            );
            """
        )
        con.execute("CREATE INDEX IF NOT EXISTS idx_digests_channel_end ON digests(channel_id, window_end);")
        con.commit()
    finally:
        con.close()


def _db_insert_digest(
    db_path: str,
    channel_id: int,
    window_start: str,
    window_end: str,
    message_count: int,
    digest_text: str,
    openai_response_id: Optional[str],
) -> None:
    con = sqlite3.connect(db_path)
    try:
        con.execute(
            """
            INSERT OR REPLACE INTO digests
              (channel_id, window_start, window_end, message_count, digest_text, openai_response_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (
                channel_id,
                window_start,
                window_end,
                message_count,
                digest_text,
                openai_response_id,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        con.commit()
    finally:
        con.close()


def _db_get_last_digest(db_path: str, channel_id: int) -> Optional[tuple]:
    con = sqlite3.connect(db_path)
    try:
        cur = con.execute(
            """
            SELECT window_start, window_end, message_count, digest_text, created_at
            FROM digests
            WHERE channel_id = ?
            ORDER BY window_end DESC
            LIMIT 1;
            """,
            (channel_id,),
        )
        return cur.fetchone()
    finally:
        con.close()


async def db_init() -> None:
    await asyncio.to_thread(_db_init, CONFIG.db_path)


async def db_insert_digest(**kwargs) -> None:
    await asyncio.to_thread(_db_insert_digest, **kwargs)


async def db_get_last_digest(channel_id: int) -> Optional[tuple]:
    return await asyncio.to_thread(_db_get_last_digest, CONFIG.db_path, channel_id)


# ----------------------------
# Transcript building
# ----------------------------

def _msg_to_line(m: discord.Message) -> str:
    ts = m.created_at.replace(tzinfo=timezone.utc).strftime("%H:%M")
    author = m.author.display_name
    content = (m.content or "").strip()

    parts = []
    if content:
        parts.append(content)

    if m.attachments:
        parts.extend([a.url for a in m.attachments])

    if m.embeds:
        for e in m.embeds:
            if e.title:
                parts.append(f"[embed title] {e.title}")
            if e.description:
                parts.append(f"[embed] {e.description}")

    body = " | ".join(parts).strip()
    if not body:
        body = "[no text]"

    return f"[{ts}] {author}: {body}"


def build_transcript(lines: List[str], window_start: datetime, window_end: datetime) -> str:
    header = (
        "You are given Discord messages from a single channel.\n"
        f"Window start (UTC): {window_start.isoformat()}\n"
        f"Window end   (UTC): {window_end.isoformat()}\n"
        "Messages (chronological):\n"
    )
    transcript = header + "\n".join(lines)
    if len(transcript) <= CONFIG.max_chars:
        return transcript

    # Keep tail if too large (recent messages usually matter most)
    trimmed_lines = []
    total = len(header)
    for line in reversed(lines):
        total += len(line) + 1
        if total > CONFIG.max_chars:
            break
        trimmed_lines.append(line)

    trimmed_lines.reverse()
    return header + "[transcript trimmed]\n" + "\n".join(trimmed_lines)


# ----------------------------
# OpenAI call
# ----------------------------

def _openai_distill(transcript: str) -> tuple[str, Optional[str]]:
    response = openai_client.responses.create(
        model=CONFIG.openai_model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=transcript,
        max_output_tokens=CONFIG.max_output_tokens,
        reasoning={"effort": "low"},
    )
    return response.output_text, getattr(response, "id", None)


async def openai_distill(transcript: str) -> tuple[str, Optional[str]]:
    return await asyncio.to_thread(_openai_distill, transcript)


# ----------------------------
# Discord bot
# ----------------------------

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True  # must be enabled in developer portal

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    log.info("Logged in as %s (id=%s)", bot.user, bot.user.id if bot.user else None)
    await db_init()
    if not hourly_digest.is_running():
        hourly_digest.start()


async def fetch_messages_for_window(
    channel: discord.TextChannel,
    window_start: datetime,
    window_end: datetime,
) -> List[discord.Message]:
    msgs: List[discord.Message] = []
    async for m in channel.history(
        after=window_start,
        before=window_end,
        oldest_first=True,
        limit=CONFIG.max_messages,
    ):
        # Skip other bots to reduce feedback loops
        if m.author.bot:
            continue
        msgs.append(m)
    return msgs


async def sleep_until_next_hour_utc():
    now = datetime.now(timezone.utc)
    next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
    await asyncio.sleep((next_hour - now).total_seconds())


@tasks.loop(hours=1)
async def hourly_digest():
    channel = bot.get_channel(CONFIG.channel_id)
    if not isinstance(channel, discord.TextChannel):
        log.warning("Channel %s unavailable or wrong type", CONFIG.channel_id)
        return

    now = datetime.now(timezone.utc)
    window_end = now.replace(minute=0, second=0, microsecond=0)
    window_start = window_end - timedelta(hours=1)

    msgs = await fetch_messages_for_window(channel, window_start, window_end)
    lines = [_msg_to_line(m) for m in msgs]
    transcript = build_transcript(lines, window_start, window_end)

    if not msgs:
        digest_text = (
            "SUMMARY:\n- No messages in this window.\n\n"
            "ANALYSIS:\n- \n\n"
            "ACTION ITEMS:\n- \n\n"
            "OPEN QUESTIONS:\n- \n\n"
            "NOTABLE QUOTES:\n- \n"
        )
        openai_id = None
    else:
        try:
            digest_text, openai_id = await openai_distill(transcript)
        except Exception:
            log.exception("OpenAI call failed")
            digest_text = (
                "SUMMARY:\n- Digest generation failed for this window.\n\n"
                "ANALYSIS:\n- \n\n"
                "ACTION ITEMS:\n- \n\n"
                "OPEN QUESTIONS:\n- \n\n"
                "NOTABLE QUOTES:\n- \n"
            )
            openai_id = None

    await db_insert_digest(
        db_path=CONFIG.db_path,
        channel_id=CONFIG.channel_id,
        window_start=window_start.isoformat(),
        window_end=window_end.isoformat(),
        message_count=len(msgs),
        digest_text=digest_text,
        openai_response_id=openai_id,
    )

    log.info("Stored digest: %s → %s (%d msgs)", window_start, window_end, len(msgs))

    if CONFIG.post_digest_to_channel:
        # Discord has message length limits; keep it safe
        out = digest_text.strip()
        if len(out) > 1900:
            out = out[:1900] + "\n…"
        await channel.send(f"**Hourly digest (UTC {window_start:%H:%M}–{window_end:%H:%M})**\n{out}")


@hourly_digest.before_loop
async def before_hourly_digest():
    await bot.wait_until_ready()
    await sleep_until_next_hour_utc()


@bot.command(name="lastdigest")
async def lastdigest(ctx: commands.Context):
    if ctx.channel.id != CONFIG.channel_id:
        await ctx.reply("This command runs in the configured channel.")
        return

    row = await db_get_last_digest(CONFIG.channel_id)
    if not row:
        await ctx.reply("No digests stored yet.")
        return

    window_start, window_end, message_count, digest_text, created_at = row
    out = digest_text.strip()
    if len(out) > 1900:
        out = out[:1900] + "\n…"

    await ctx.reply(
        f"**Last digest**\n"
        f"Window (UTC): {window_start} → {window_end}\n"
        f"Messages: {message_count}\n"
        f"Stored: {created_at}\n\n"
        f"{out}"
    )


if __name__ == "__main__":
    bot.run(CONFIG.discord_token)
