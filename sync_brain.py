#!/usr/bin/env python3
"""
Two-way sync between a local `brain/` folder and your Supabase brain.

This is what makes your memory bidirectional. Your AIs (Claude Code, Codex, ...)
read and write plain markdown files in the local `brain/` folder. This script
mirrors that folder to your Supabase `brain_files` table and back:

    local brain/  <-->  Supabase brain_files

So when Claude learns something and writes a file into brain/, this pushes it to
the cloud, and the next time Codex syncs, it pulls that same fact down. New
memory from ANY tool ends up in one place every other tool can see. (Telegram
voice notes land in Supabase too, so they flow down into brain/ the same way.)

Newer-wins by timestamp. It never deletes anything — safe to run on a loop.

Usage:
    python3 sync_brain.py            # sync once and exit
    python3 sync_brain.py --loop     # keep running, sync every 60s

Only needs SUPABASE_URL and SUPABASE_KEY in your .env.
"""

import datetime as dt
import os
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / ".env"
BRAIN_DIR = HERE / "brain"


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
    for k in ("SUPABASE_URL", "SUPABASE_KEY"):
        if not env.get(k):
            sys.exit(f"Missing in .env: {k}")
    return env


# --------------------------------------------------------------------------- #
# Supabase — same calls the bot and fetch_context already use
# --------------------------------------------------------------------------- #
def fetch_rows(url, key):
    r = requests.get(
        f"{url.rstrip('/')}/rest/v1/brain_files",
        params={"select": "path,content,updated_at", "order": "updated_at.desc"},
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def upsert_row(url, key, path, content, updated_at):
    r = requests.post(
        f"{url.rstrip('/')}/rest/v1/brain_files",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        },
        json={"path": path, "content": content, "updated_at": updated_at},
        timeout=30,
    )
    r.raise_for_status()


# --------------------------------------------------------------------------- #
# Local brain/ folder helpers
# --------------------------------------------------------------------------- #
def parse_ts(value):
    """Parse a Supabase timestamptz into an aware UTC datetime."""
    if not value:
        return dt.datetime.fromtimestamp(0, dt.timezone.utc)
    text = value.replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        return dt.datetime.fromtimestamp(0, dt.timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def local_files():
    """Map of 'relative/path.md' -> (Path, mtime as aware UTC datetime)."""
    out = {}
    if not BRAIN_DIR.exists():
        return out
    for p in BRAIN_DIR.rglob("*.md"):
        if not p.is_file():
            continue
        rel = p.relative_to(BRAIN_DIR).as_posix()
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc)
        out[rel] = (p, mtime)
    return out


def write_local(rel_path, content, updated_at):
    dest = BRAIN_DIR / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content)
    # Stamp the file's mtime to match the cloud row so it won't re-push next run.
    ts = updated_at.timestamp()
    os.utime(dest, (ts, ts))


# --------------------------------------------------------------------------- #
# The sync
# --------------------------------------------------------------------------- #
def sync_once(env):
    url, key = env["SUPABASE_URL"], env["SUPABASE_KEY"]
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)

    cloud = {row["path"]: row for row in fetch_rows(url, key)}
    local = local_files()
    pulled = pushed = 0

    # Cloud -> local: bring down anything new or newer in the cloud.
    for path, row in cloud.items():
        cloud_ts = parse_ts(row.get("updated_at"))
        if path not in local or cloud_ts > local[path][1] + dt.timedelta(seconds=1):
            write_local(path, row.get("content", ""), cloud_ts)
            pulled += 1

    # Local -> cloud: push up anything new or newer on disk.
    for path, (fpath, mtime) in local.items():
        row = cloud.get(path)
        cloud_ts = parse_ts(row.get("updated_at")) if row else None
        if row is None or mtime > cloud_ts + dt.timedelta(seconds=1):
            upsert_row(url, key, path, fpath.read_text(), mtime.isoformat())
            pushed += 1

    print(f"synced: pulled {pulled} down, pushed {pushed} up "
          f"({len(cloud)} cloud / {len(local)} local files)")


def main():
    env = load_env()
    if "--loop" not in sys.argv:
        sync_once(env)
        return
    print("Brain sync running. Your AIs read/write brain/, this mirrors it to the "
          "cloud. Ctrl+C to stop.")
    while True:
        try:
            sync_once(env)
        except requests.RequestException as exc:
            print(f"(temporary network issue, will retry): {exc}")
        time.sleep(60)


if __name__ == "__main__":
    main()
