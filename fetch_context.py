#!/usr/bin/env python3
"""
Pull every row out of your Supabase brain and write it into one local file,
MY_CONTEXT.md. This makes your memory readable by ANY AI tool — even ones
that can't make network calls themselves (plain GitHub Copilot, a plain
ChatGPT paste, etc.) — because every coding tool can read a local file.

Usage:
    python3 fetch_context.py

Run it whenever you want your local snapshot refreshed (or schedule it, e.g.
every few minutes, the same way second_brain_bot.py runs).
"""

import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / ".env"
OUTPUT_FILE = HERE / "MY_CONTEXT.md"


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
    return env


def fetch_all_rows(url, key):
    r = requests.get(
        f"{url.rstrip('/')}/rest/v1/brain_files",
        params={"select": "path,content,updated_at", "order": "updated_at.desc"},
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main():
    env = load_env()
    rows = fetch_all_rows(env["SUPABASE_URL"], env["SUPABASE_KEY"])

    lines = ["# My AI Context (auto-generated — do not edit by hand)\n"]
    for row in rows:
        lines.append(f"## {row['path']}\n{row['content']}\n")

    OUTPUT_FILE.write_text("\n".join(lines))
    print(f"Wrote {len(rows)} entries to {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
