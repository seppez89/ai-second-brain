# 🧠☁️ Second Brain Starter

Give your AI a memory it never loses — in the cloud, that **you** own, that works
in every app.

You send a voice note (or text) to a Telegram bot. It gets transcribed for free
and saved into your own Supabase database. Your AI reads that database as memory.

**100% free stack:** Telegram + [Groq](https://console.groq.com) (transcription) +
[Supabase](https://supabase.com) (database).

> It's not about the perfect prompt. It's about **context**. Every answer your AI
> gives is only as good as what it knows about you. This gives it that — permanently.

---

## What you'll need (all free, ~10 minutes)

Three accounts and five keys. Grab them in this order.

### 1. Supabase — your cloud brain
1. Go to [supabase.com](https://supabase.com) → **Start your project** → sign in with GitHub.
2. **New project** → name it `second-brain` → generate a password (save it) → pick your closest region → **Create** (wait ~2 min).
3. Left sidebar → **SQL Editor** → **New query** → paste the contents of [`supabase_setup.sql`](./supabase_setup.sql) → **Run**. ("Success. No rows returned" is correct.)
4. Left sidebar → **Project Settings → API Keys**. Copy two things:
   - **Project URL** → `https://xxxx.supabase.co`
   - **Secret key** → the one starting `sb_secret_...`
     ⚠️ Use the **secret** key, *not* the publishable one — the publishable key can't write.

### 2. Telegram — your voice bot
1. In Telegram, search **@BotFather** → send `/newbot`.
2. Give it a name, then a username ending in `bot`.
3. BotFather sends you a **token** — copy it.
4. Open your **new bot** and send it any message (say "hi").

### 3. Groq — free voice-to-text
1. Go to [console.groq.com](https://console.groq.com) → sign up (no card).
2. **API Keys → Create API Key** → copy it.

---

## Wire it up

1. **Install Python** (3.9+) if you don't have it, then install the one dependency:
   ```
   pip3 install requests
   ```
2. Copy `.env.example` to `.env` and paste in your keys:
   ```
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...        # get this in the next step
   GROQ_API_KEY=...
   SUPABASE_URL=...
   SUPABASE_KEY=...
   ```
3. **Get your `TELEGRAM_CHAT_ID`** (10 seconds): after you've messaged your bot,
   open this link in your browser (paste your bot token in):
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Find `"chat":{"id":123456789` — that number is your chat id. Put it in `.env`.

---

## Run it

Test it once:
```
python3 second_brain_bot.py
```
Send your bot a voice note, run that again — you'll see `saved: ...`, and the note
appears as a row in your Supabase table (**Table Editor → brain_files**). 🎉

### Keep it running automatically
So it catches your notes without you doing anything, leave it looping:
```
python3 second_brain_bot.py --loop
```
It checks every 60 seconds. Keep that terminal open, or run it on an always-on
machine / cheap cloud box. (On Mac/Linux you can also schedule it with `cron`; on
Windows use Task Scheduler.)

---

## Connect your AI to the brain
Any AI tool that can reach the internet or read files can now use this memory.
The simplest version: point a coding assistant (Claude Code, Codex) at your
Supabase project, or export the rows into a file it reads at the start of a chat.

---

## Safety
- Your `.env` holds your passwords — it's git-ignored, never share or commit it.
- Blur your keys if you screen-record.

Built something cool with it? Enjoy your second brain. 🧠
