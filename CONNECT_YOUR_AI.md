# 🔌 Wire your AIs to the brain — both directions

This is the part that matters most. It's not just "let my AI read some notes."
It's a **loop**: every AI you use reads the brain before it answers, and writes
what it learns back into it — so your memory keeps growing no matter which tool
you happen to be in.

```
   Claude Code ──write──┐                 ┌──write── Codex
        │               ▼                 ▼            │
       read   ┌───────────────────────────────┐     read
        └──────│   brain/  (local)  <->  Supabase │──────┘
               └───────────────────────────────┘
                              ▲
                              │  (optional) Telegram voice notes drop in here
```

The pieces:

- **`brain/`** — a local folder of plain markdown files. This is where your AIs
  actually read and write. One file = one memory.
- **`sync_brain.py`** — mirrors `brain/` to your Supabase database and back,
  newer-wins, every 60 seconds. This is how a fact Claude writes reaches Codex,
  and how Codex's notes (or a Telegram voice note) reach Claude.

Run the sync on a loop and leave it going:

```
python3 sync_brain.py --loop
```

Now set up each tool. There are two ways to give a tool write-back; use whichever
the tool supports.

---

## Claude Code

**Reading** — drop a `CLAUDE.md` in your project root:

```md
# My second brain
Before answering anything about me, my work, or my projects, read the markdown
files in the ./brain folder — that's my personal memory. Treat it as the source
of truth about me.

When I tell you to remember something, or you learn a durable new fact about me
or my projects, SAVE it as a new markdown file in ./brain (a short title, then
the fact). Keep one fact per file. Don't duplicate a fact that's already there —
update the existing file instead.
```

That already gives you both directions: Claude reads `brain/`, and writes new
memories into it as files. `sync_brain.py` carries them to the cloud.

**The automatic upgrade (best):** Claude Code has its own built-in memory feature
— when it decides something is worth remembering, it writes a file into its
project memory directory *on its own*, no instruction needed. Point that
directory at your `brain/` folder (a one-time symlink) and Claude's native
memories land straight in your brain with zero reliance on it "remembering to."
This is the most reliable write-back there is. In Easy Mode the setup prompt does
this for you; the `CLAUDE.md` above is the universal fallback if you'd rather not
touch the symlink.

---

## Codex

Codex reads its instructions from `AGENTS.md`. Use `~/.codex/AGENTS.md` to make
it apply everywhere, or a project-root `AGENTS.md` for just one project:

```md
# My second brain
Before answering anything that needs my personal or business context, read the
markdown files in the brain/ folder of my second-brain project — that's my
memory. Treat it as authoritative context about me.

When you learn a durable new fact about me or my projects (or I tell you to
remember something), write it as a new markdown file in that brain/ folder — a
short title, then the fact, one fact per file. Update the existing file instead
of duplicating if the fact is already there.
```

Codex's write-back is instruction-following (it does it because you told it to,
not via a built-in memory feature), so it's a little less guaranteed than
Claude's native path — but it works, and `sync_brain.py` pushes whatever it
writes up to the cloud for Claude to pick up.

---

## The loop in action

1. You're working in **Claude**. It learns your business is now a Pty Ltd. It
   writes `brain/company-structure.md`.
2. `sync_brain.py` pushes that file to Supabase within a minute.
3. Later you open **Codex** on a totally different task. Its sync has pulled the
   new file down into `brain/`, so when it reads your brain, it already knows
   you're a Pty Ltd. You never told it.

That's the whole idea — **one memory, every tool keeping it current for the next
one.** Because it lives in your own Supabase, it's not locked inside Anthropic's
walls or OpenAI's. It's yours.

---

## Other tools (quick note)

The same brain works with anything, it just may not write back automatically:

- **GitHub Copilot (agent mode):** `.github/copilot-instructions.md` with the same
  read/write instruction as Codex above (needs terminal access).
- **ChatGPT / any web chat:** run `python3 fetch_context.py` to export your whole
  brain into one file, `MY_CONTEXT.md`, and paste or upload it at the start of a
  chat. It reads; it won't write back on its own.

But the heart of the system is the Claude + Codex loop above. Get that running
and your memory takes care of itself.
