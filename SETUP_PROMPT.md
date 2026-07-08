# 🚀 Easy Mode — let Claude set it up for you

Don't want to touch the code yourself? You don't have to.

1. Install **Claude Code** (or use **Codex**) — the free "builder" version of the AI.
2. Open it in an empty folder.
3. Paste the prompt below and hit enter.

Claude will do the technical parts for you and just ask you for the things only
you can get (your account keys), one at a time, in plain English.

---

## Copy this prompt

```
Help me set up "ai-second-brain" — a system where I send voice notes to a
Telegram bot and they get transcribed and saved into my own Supabase cloud
database, giving my AI a memory it never loses.

The code is here: https://github.com/seppez89/ai-second-brain

Walk me through the whole setup. Do everything you can for me, and ask me for
only what I personally have to provide. Go ONE step at a time and wait for me
before moving on. Keep it beginner-friendly and explain each step in plain
English. Specifically:

1. Clone the repo into this folder and install the one dependency (requests).
2. Guide me to create three free accounts and collect 5 values, one at a time,
   explaining each as we go:
   - Telegram bot token (via @BotFather)
   - my Telegram chat id (help me get this automatically after I message the bot)
   - Groq API key (console.groq.com)
   - Supabase Project URL and secret key (supabase.com)
3. Help me run the table setup SQL from supabase_setup.sql in Supabase.
4. Create the .env file with my keys. Never commit it.
5. Run the bot once and confirm my voice note appears as a row in Supabase.
6. Set it to keep running so it catches my notes automatically.

Before you start, briefly tell me what I'll need and how long it'll take.
```

---

That's it. You talk, it builds. Welcome to your second brain. 🧠
