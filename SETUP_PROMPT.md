# 🚀 Easy Mode — let the AI wire it up for you

The whole point of this system: **one memory that every AI you use both reads
from and writes to.** When Claude learns something about you, Codex knows it too.
When Codex figures something out, Claude picks it up. Nothing gets re-explained,
and nothing stays trapped in one app.

You don't have to build any of that yourself. Open **Claude Code** (or **Codex**)
in an empty folder, paste the prompt below, and it does the technical parts —
asking you only for the few things that have to come from you.

> New to this? "Claude Code" and "Codex" are the *builder* versions of Claude and
> ChatGPT that can create files and run commands on your computer. Claude Code
> needs a paid Claude plan; the rest of this system is free.

---

## Copy this prompt

```
Help me set up my "second brain" — one memory store that every AI I use both
READS from and WRITES back to, so Claude and Codex share the same picture of me
and I never have to re-explain my context.

The code is here: https://github.com/seppez89/ai-second-brain

Walk me through the whole setup ONE step at a time and wait for me before moving
on. Keep it beginner-friendly and explain each step in plain English. Do
everything you can for me; only ask me for the things I personally have to get.

=== PART 1: the cloud brain (my source of truth) ===
1. Clone the repo into this folder and install the one dependency (requests).
2. Help me create a free Supabase account and collect two values, explaining
   each as we go: my Project URL and my secret key (sb_secret_...).
3. Help me run the table setup SQL from supabase_setup.sql in Supabase.
4. Create the .env file with those two keys. Never commit it.

=== PART 2: wire Claude + Codex to read AND write the brain (the main event) ===
Read CONNECT_YOUR_AI.md, then set this up for the tools I actually use — ask me
which ones (Claude Code, Codex, or both):

5. Set up the local `brain/` folder as the working copy of my memory, and get
   `sync_brain.py` running on a loop so that folder stays mirrored to Supabase
   both directions (my machine <-> cloud) automatically.
6. Wire Claude Code so it READS my brain before answering AND writes durable new
   facts about me back into it — the automatic way if possible (point Claude
   Code's own memory directory at the brain/ folder), otherwise via a CLAUDE.md
   instruction. Explain which one you did and why.
7. Wire Codex the same way via ~/.codex/AGENTS.md: read the brain before
   context-heavy answers, and write durable new facts back into brain/.
8. PROVE it works: save one test fact through Claude (e.g. tell it to remember
   something about me), run the sync, and show me that same fact arriving in
   Supabase — and explain how Codex would now pick it up on its next sync.

=== PART 3 (optional): talk to your brain by voice ===
9. If I want it, also set up the Telegram voice bot (second_brain_bot.py) so I
   can send voice notes that get transcribed for free (Groq) and dropped into
   the brain. This is a bonus input, not the core — ask me if I want it before
   setting it up, and only then collect the Telegram + Groq keys.

Before you start, briefly tell me the parts, what I'll need to grab, and roughly
how long it'll take.
```

---

That's it. You talk, it wires everything together. From here on, every AI you
point at your brain already knows you — and keeps it up to date for the next one. 🧠
