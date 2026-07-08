# 🔌 Connect ANY AI to your brain

This is the part that makes it AI-agnostic — not just Claude, not just ChatGPT.
**Any tool that can read a file or make a web request can use this memory.**

There are two methods. Use whichever fits the tool.

---

## Method 1 — The universal way (works with literally everything)

A tiny script pulls everything out of your Supabase brain into one local file,
`MY_CONTEXT.md`. Then you tell your AI tool — any AI tool — to read that file
before answering. Since every coding assistant (and every chat tool you can
paste text into) can read a local file, this always works, no exceptions.

```
python3 fetch_context.py
```

That's it. Run it anytime you want the snapshot refreshed (or leave it running
on a timer, the same way `second_brain_bot.py` does). Then:

- **Claude Code / Cursor / Codex / any coding AI:** tell it once — *"Always read
  MY_CONTEXT.md before answering questions about me."* It'll remember for the
  session (make it permanent with Method 2 below).
- **GitHub Copilot (Chat, no agent mode):** open `MY_CONTEXT.md` in a tab, or
  paste it into the chat — Copilot reads whatever's open/referenced in your
  editor.
- **ChatGPT / any web chat:** paste the contents of `MY_CONTEXT.md` at the start
  of a conversation, or upload it as a file if the tool supports uploads.

---

## Method 2 — Live & automatic (for tools that can run commands)

Claude Code, Codex, and Copilot's **agent mode** can all execute commands
themselves. Instead of a static snapshot, give them a standing instruction to
pull your brain **fresh, every time**, straight from Supabase — no local file
needed. This is the "always current" version.

The raw call every tool uses under the hood is one HTTP GET:

```
GET {SUPABASE_URL}/rest/v1/brain_files?select=path,content&order=updated_at.desc
Headers:
  apikey: {SUPABASE_KEY}
  Authorization: Bearer {SUPABASE_KEY}
```

Drop the matching instructions file into your project so each tool picks it up
automatically:

### Claude Code → `CLAUDE.md` (project root)
```md
# Personal context
Before answering anything that needs my personal/business context, fetch my
second brain:
  curl -s "{SUPABASE_URL}/rest/v1/brain_files?select=path,content" \
    -H "apikey: {SUPABASE_KEY}" -H "Authorization: Bearer {SUPABASE_KEY}"
Read the results as context about me.
```

### Codex → `AGENTS.md` (project root, or `~/.codex/AGENTS.md` for global)
```md
# Personal context
Before answering questions needing my personal/business context, run:
  curl -s "{SUPABASE_URL}/rest/v1/brain_files?select=path,content" \
    -H "apikey: {SUPABASE_KEY}" -H "Authorization: Bearer {SUPABASE_KEY}"
Treat the response as authoritative context about me.
```

### GitHub Copilot → `.github/copilot-instructions.md` (repo root)
```md
# Personal context
When relevant, fetch my second brain via:
  curl -s "{SUPABASE_URL}/rest/v1/brain_files?select=path,content" \
    -H "apikey: {SUPABASE_KEY}" -H "Authorization: Bearer {SUPABASE_KEY}"
(Requires Copilot's agent mode with terminal access. On plain Copilot Chat,
use Method 1 instead — it can't make network calls on its own.)
```

Replace `{SUPABASE_URL}` and `{SUPABASE_KEY}` with your real values from `.env`.

---

## Which method should you use?

| Tool | Recommended method |
|---|---|
| Claude Code | Method 2 (`CLAUDE.md`) — live, automatic |
| Codex | Method 2 (`AGENTS.md`) — live, automatic |
| Copilot, agent mode | Method 2 (`.github/copilot-instructions.md`) |
| Copilot, plain chat | Method 1 — open/paste `MY_CONTEXT.md` |
| ChatGPT / any web chat | Method 1 — paste or upload `MY_CONTEXT.md` |

**The point:** your brain lives in Supabase, not inside any one AI company's
walls. Point whatever tool you're using at it, and it already knows you.
