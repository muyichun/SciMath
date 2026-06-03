# AGENTS.md

> Project author: **xujing**

Instructions for all AI coding agents (Claude Code, Codex, Cursor, etc.) working on this repository.

---

## Mandatory documentation update after every session

After any session that modifies source code, you **must** update the following files before finishing:

| File | When to update | What to write |
|------|---------------|---------------|
| `docs/DEV_LOG.md` | Every session with code changes | New entry: date, agent, summary of changes |
| `CLAUDE.md` | When file structure or architecture changes | Update Architecture section |
| `README.md` | When new tools or features are added | Update Features / Usage sections |
| `AGENTS.md` | When workflow or conventions change | Update the relevant section |

> **Rule**: If you changed `.py` or `.yaml` files under `tools/` or `provider/`, you must append a dev log entry. No exceptions.

---

## Dev log entry format (`docs/DEV_LOG.md`)

Append to the top of the file (newest first):

```markdown
## YYYY-MM-DD — <Agent Name>

**Changes:**
- <what was added/changed/fixed, one bullet per logical change>

**Files modified:**
- `path/to/file.py` — one-line description
```

Use the actual date. For agent name use: `Claude Code`, `Codex`, `Cursor`, or `xujing`.

---

## Project overview

A Dify plugin providing math tools. Each tool is a pair of files:
- `tools/<name>.py` — Python implementation of `Tool._invoke()`
- `tools/<name>.yaml` — Dify tool schema (parameters, labels, description)

All tools are registered in `provider/maths.yaml` under `tools:`.

See `CLAUDE.md` for full architecture details.

---

## Multi-tool workflow

This project is developed by multiple AI agents:

| Agent | Config file read | Notes |
|-------|-----------------|-------|
| Claude Code | `CLAUDE.md`, `AGENTS.md` | Primary development environment |
| Codex (OpenAI) | `AGENTS.md` | Reads this file by default |
| Cursor | `CLAUDE.md`, `AGENTS.md` | Reads both if present |

**Coordination protocol:**
1. Each agent reads `docs/DEV_LOG.md` to understand what was done before starting.
2. Each agent commits with a clear message describing the change.
3. Each agent appends a dev log entry immediately after finishing.

---

## Adding a new tool (checklist)

- [ ] `tools/<name>.py` — implement `class <Name>Tool(Tool)` with `_invoke()`
- [ ] `tools/<name>.yaml` — define schema (description, identity, parameters)
- [ ] Register in `provider/maths.yaml` under `tools:`
- [ ] Update `docs/DEV_LOG.md`
- [ ] Update `CLAUDE.md` Architecture section
- [ ] Update `README.md` Features section

---

## Code conventions

- Dependencies: managed via `uv` (`pyproject.toml`)
- All tools return both `create_text_message` (human-readable + LaTeX) and `create_json_message` (structured)
- Shared utilities go in `tools/sympy_utils.py` (or similar `tools/*_utils.py`)
- No comments unless the WHY is non-obvious
