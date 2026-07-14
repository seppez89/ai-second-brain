# 🧠☁️ Second Brain Starter

Give every AI you use **one shared memory** — that reads and writes itself, lives
in the cloud, and that **you** own.

When Claude learns something about you, Codex knows it too. When Codex figures
something out, Claude picks it up. Nothing gets re-explained, and nothing stays
trapped inside one company's app.

> It's not about the perfect prompt. It's about **context**. Every answer your AI
> gives is only as good as what it knows about you. This gives it that — once,
> permanently, everywhere.

**The core stack is free:** [Supabase](https://supabase.com) (your cloud brain) +
the builder AIs you already use. *(A paid Claude plan is needed for Claude Code
itself; Supabase is free. The optional voice bot adds Telegram + Groq, also free.)*

---

## 🚀 Two ways to do this

**Easy mode (recommended):** don't touch the code — let the AI wire it up *for*
you. Open **Claude Code** (or Codex), paste the prompt in
**[SETUP_PROMPT.md](./SETUP_PROMPT.md)**, and it does everything, asking only for
the couple of keys you personally need to grab. This is the way. 👇

**Manual mode:** prefer to do it yourself? Follow the steps below.

---

## How it works (the loop)

```
   Claude Code ──write──┐                 ┌──write── Codex
        │               ▼                 ▼            │
       read   ┌───────────────────────────────┐     read
        └──────│   brain/  (local)  <->  Supabase │──────┘
               └───────────────────────────────┘
                              ▲
                              │  (optional) Telegram voice notes drop in here
```

- **`brain/`** — a local folder of plain markdown files. One file = one memory.
  Your AIs read these before they answer and write new ones as they learn.
- **Supabase** — the cloud copy you own; the shared hub every tool syncs with.
- **`sync_brain.py`** — mirrors `brain/` ⇄ Supabase both directions, so a fact
  one tool writes reaches every other tool.

---

## Setup

### 1. Supabase — your cloud brain (the only account you *need*)
1. Go to [supabase.com](https://supabase.com) → **Start your project** → sign in with GitHub.
2. **New project** → name it `second-brain` → generate a password (save it) → pick your closest region → **Create** (wait ~2 min).
3. Left sidebar → **SQL Editor** → **New query** → paste the contents of [`supabase_setup.sql`](./supabase_setup.sql) → **Run**. ("Success. No rows returned" is correct.)
4. Left sidebar → **Project Settings → API Keys**. Copy two things:
   - **Project URL** → `https://xxxx.supabase.co`
   - **Secret key** → the one starting `sb_secret_...`
     ⚠️ Use the **secret** key, *not* the publishable one — the publishable key can't write.

### 2. Wire it up
1. **Install Python** (3.9+) if you don't have it, then the one dependency:
   ```
   pip3 install requests
   ```
2. Copy `.env.example` to `.env` and paste in your two Supabase keys:
   ```
   SUPABASE_URL=...
   SUPABASE_KEY=...
   ```
   (The Telegram/Groq lines are only for the optional voice bot — leave them for now.)
3. Start the two-way sync and leave it running:
   ```
   python3 sync_brain.py --loop
   ```
   It mirrors your local `brain/` folder to Supabase and back every 60 seconds.

### 3. Connect Claude + Codex — read AND write
This is the whole point. Give each tool a standing instruction to read your
`brain/` folder before answering and write new memories back into it.

**Full copy-paste instructions for each tool → [CONNECT_YOUR_AI.md](./CONNECT_YOUR_AI.md)**

Quick version: drop a `CLAUDE.md` (for Claude Code) and an `AGENTS.md` (for
Codex) that say *"read the `brain/` folder as my memory; when you learn a durable
fact about me, save it there as a new markdown file."* From then on, both tools
share — and keep growing — the same memory.

---

## (Optional) Talk to your brain by voice

Want to add memories just by talking? The included Telegram bot transcribes voice
notes for free and drops them into your brain. It's a **bonus input**, not the
core — skip it if you just want the Claude ↔ Codex loop.

<details>
<summary>Set up the voice bot</summary>

Grab two more free keys:

- **Telegram bot token** — in Telegram, message **@BotFather** → `/newbot` → name
  it, give it a username ending in `bot` → copy the **token**. Open your new bot
  and send it any message.
- **Groq API key** — [console.groq.com](https://console.groq.com) → sign up (no
  card) → **API Keys → Create API Key** → copy it.

Add all four remaining values to `.env` (`TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`,
`SUPABASE_URL`, `SUPABASE_KEY`), then get your `TELEGRAM_CHAT_ID`: after messaging
your bot, open `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` and find
`"chat":{"id":123456789` — that number goes in `.env`.

Run it:
```
python3 second_brain_bot.py            # check once
python3 second_brain_bot.py --loop     # keep running, checks every 60s
```
Send a voice note, and it lands in Supabase → `sync_brain.py` pulls it into
`brain/` → every AI sees it.
</details>

---

## Safety
- Your `.env` holds your keys — it's git-ignored, never share or commit it.
- Blur your keys if you screen-record.

Enjoy your second brain. 🧠
