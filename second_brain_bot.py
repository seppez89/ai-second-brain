#!/usr/bin/env python3
"""
Second Brain Bot — send a voice note (or text) to your Telegram bot, and it gets
transcribed and saved into your own Supabase cloud database. Your AI can then
read that database as memory, from any app.

Free stack:  Telegram (bot)  +  Groq (free transcription)  +  Supabase (free DB)

Setup: copy .env.example to .env, paste in your 5 keys, then run:

    python3 second_brain_bot.py            # check once and exit
    python3 second_brain_bot.py --loop     # keep running, check every 60s

See README.md for the click-by-click.
"""

import datetime as dt
import json
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / ".env"
STATE_FILE = HERE / ".state.json"  # remembers the last message we processed


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
def load_env():
    if not ENV_FILE.exists():
        sys.exit("No .env file found. Copy .env.example to .env and fill it in.")
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip().strip('"').strip("'")
    required = [
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "GROQ_API_KEY",
        "SUPABASE_URL",
        "SUPABASE_KEY",
    ]
    missing = [k for k in required if not env.get(k)]
    if missing:
        sys.exit(f"Missing in .env: {', '.join(missing)}")
    return env


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_update_id": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state))


# --------------------------------------------------------------------------- #
# Telegram
# --------------------------------------------------------------------------- #
def get_updates(token, offset):
    r = requests.get(
        f"https://api.telegram.org/bot{token}/getUpdates",
        params={"offset": offset, "timeout": 0},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["result"]


def download_file(token, file_id):
    r = requests.get(
        f"https://api.telegram.org/bot{token}/getFile",
        params={"file_id": file_id},
        timeout=30,
    )
    r.raise_for_status()
    path = r.json()["result"]["file_path"]
    f = requests.get(f"https://api.telegram.org/file/bot{token}/{path}", timeout=60)
    f.raise_for_status()
    return f.content


# --------------------------------------------------------------------------- #
# Groq — free, fast voice-to-text
# --------------------------------------------------------------------------- #
def transcribe(groq_key, audio_bytes):
    r = requests.post(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {groq_key}"},
        files={"file": ("voice.ogg", audio_bytes, "audio/ogg")},
        data={"model": "whisper-large-v3"},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["text"].strip()


# --------------------------------------------------------------------------- #
# Supabase — your cloud brain
# --------------------------------------------------------------------------- #
def save_to_supabase(env, text, when):
    """Each note becomes one row in the brain_files table, keyed by timestamp."""
    url = env["SUPABASE_URL"].rstrip("/")
    key = env["SUPABASE_KEY"]
    row = {
        "path": f"journal/{when.isoformat()}",
        "content": text,
        "updated_at": when.astimezone(dt.timezone.utc).isoformat(),
    }
    r = requests.post(
        f"{url}/rest/v1/brain_files",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        },
        json=row,
        timeout=30,
    )
    r.raise_for_status()


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def check_once(env):
    token = env["TELEGRAM_BOT_TOKEN"]
    chat_id = str(env["TELEGRAM_CHAT_ID"])
    state = load_state()

    for update in get_updates(token, state["last_update_id"] + 1):
        message = update.get("message")
        # Ignore anything not from your own chat.
        if message and str(message.get("chat", {}).get("id")) == chat_id:
            when = dt.datetime.fromtimestamp(message["date"])
            text = None
            if "voice" in message or "audio" in message:
                media = message.get("voice") or message["audio"]
                text = transcribe(env["GROQ_API_KEY"], download_file(token, media["file_id"]))
            elif "text" in message and not message["text"].startswith("/"):
                text = message["text"]

            if text:
                save_to_supabase(env, text, when)
                print(f"saved: {text[:60]}{'...' if len(text) > 60 else ''}")

        state["last_update_id"] = max(state["last_update_id"], update["update_id"])
        save_state(state)


def main():
    env = load_env()
    loop = "--loop" in sys.argv
    if not loop:
        check_once(env)
        return
    print("Second Brain Bot running. Send your Telegram bot a voice note. Ctrl+C to stop.")
    while True:
        try:
            check_once(env)
        except requests.RequestException as exc:
            print(f"(temporary network issue, will retry): {exc}")
        time.sleep(60)


if __name__ == "__main__":
    main()
