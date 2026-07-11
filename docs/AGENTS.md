# Dumbledore — Developer Guide

## Project Overview

Dumbledore is a Socratic AI Telegram bot that challenges thinking on system design, DSA, and software architecture in group chats.

**Bot:** @dumbledore_arch_bot  
**Repo:** https://github.com/dev-shridhar/dumbledore  
**LLM Chain:** Ollama (local, not ready) → Groq API (working)

---

## Git Workflow

1. **Never commit directly to `main`.**
2. Always create a feature branch: `feat/<name>` or `fix/<name>`
3. Push the branch and open a PR against `main`
4. CI checks must pass before merging
5. Squash or merge commit — no force pushes to `main`

### Branch Naming

- `feat/` — new features
- `fix/` — bug fixes
- `chore/` — maintenance, deps, config
- `docs/` — documentation only

---

## CI/CD Pipeline

Defined in `.github/workflows/tests.yml`. Runs on every PR and push to `main`.

### Required Checks (all must pass)

| Check Name | What It Does |
|---|---|
| `Tests / tests (3.10)` | Lint + typecheck + tests on Python 3.10 |
| `Tests / tests (3.11)` | Lint + typecheck + tests on Python 3.11 |
| `Tests / tests (3.12)` | Lint + typecheck + tests on Python 3.12 |

### What CI Runs (in order)

1. **ruff check** — linting (line length 100, select E/F/I/W rules)
2. **mypy** — type checking (ignore missing imports)
3. **pytest** — unit tests (`tests/` directory)

### Running Locally Before Pushing

```bash
pip install -r requirements.txt
pip install pytest ruff mypy

ruff check .
mypy --ignore-missing-imports .
pytest tests/ -v
```

All 3 must pass with zero errors before pushing.

---

## Code Style

- **Formatter/Linter:** ruff (line length 100, target Python 3.10)
- **Type checker:** mypy (ignore missing imports, non-strict)
- **Test runner:** pytest
- **No comments** in code unless explicitly asked
- Follow existing patterns — check neighboring files before writing new code
- Use `from __future__ import annotations` at the top of every file

---

## Project Structure

```
├── main.py              # Telegram bot handlers and entry point
├── brain.py             # Versioned prompt loader and message builder
├── llm.py               # Ollama primary + Groq fallback chat client
├── memory.py            # Per-group chat history buffer
├── config.py            # .env loading, Config dataclass
├── start_bot.py         # Entry point (loads .env, calls main)
├── prompts/
│   ├── __init__.py      # VERSION = "1.0.0"
│   ├── challenge_v1.py  # Socratic questioning prompt
│   ├── ask_v1.py        # Expert answer prompt
│   └── conclude_v1.py   # Discussion summary prompt
├── tests/
│   ├── conftest.py      # sys.path fix for CI
│   ├── test_brain.py    # Prompt loading and message building
│   ├── test_llm.py      # Ollama/Groq fallback
│   └── test_memory.py   # Group memory
├── requirements.txt     # Pinned dependencies
├── pyproject.toml       # ruff, mypy, pytest config
└── .env                 # Secrets (gitignored)
```

---

## Prompts

Prompts are **versioned** in the `prompts/` directory. Each prompt type has its own file.

### Adding/Updating Prompts

1. Create or edit `prompts/<type>_v<N>.py` (e.g., `challenge_v2.py`)
2. Update `prompts/__init__.py` — bump `VERSION` and update mappings
3. Both old and new versions must coexist (no breaking changes)
4. Update tests in `tests/test_brain.py`

### Prompt Types

| Type | Command | Purpose |
|---|---|---|
| `challenge` | Reply to any message | Socratic probing of reasoning |
| `ask` | `/ask <question>` | Direct expert answer |
| `conclude` | `/conclude` | Summarize discussion with correct answer |

---

## Bot Commands

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/help` | Same as /start |
| `/ask <question>` | Direct expert answer |
| `/conclude` | Summarize with correct answer |
| `/clear` | Reset group memory |
| `/status` | Show buffer count, prompt version, model |
| `/prompts` | Show current prompt version |

---

## Security

- **Never commit secrets** — `.env` is gitignored, use GitHub Secrets for CI
- **Rotate keys** if shared in chat — old Telegram token was already revoked once
- GitHub Secrets required: `TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`
- `.env.example` should exist with placeholder values (no real keys)

---

## Bot Name

- Correct spelling: **dumbledore** (lowercase)
- Not "dumbeldore" or any other variation
- Telegram handle: @dumbledore_arch_bot

---

## Deployment

**Entry point:** `python start_bot.py`

### PythonAnywhere

See `DEPLOY.md` for PythonAnywhere instructions. Requires $10/month Developer plan for always-on tasks.

---

## Testing

- **20 tests** across 3 Python versions (3.10, 3.11, 3.12)
- Tests cover: prompt loading, message building, LLM fallback, group memory
- Run: `pytest tests/ -v`
- Coverage: aim for new code to have corresponding tests
- Test files follow `test_<module>.py` naming

---

## Dependencies

Pinned in `requirements.txt`:

```
python-telegram-bot==21.3
openai==1.45.0
httpx==0.27.2
python-dotenv==1.0.1
```

- Add new deps with `pip install <package>==<version>` then update `requirements.txt`
- Never use unpinned versions in `requirements.txt`

---

## Quick Reference

```bash
# Local dev
pip install -r requirements.txt
python start_bot.py

# Run checks
ruff check .
mypy --ignore-missing-imports .
pytest tests/ -v

# Create PR
git checkout -b feat/my-feature
git add . && git commit -m "feat: description"
git push -u origin feat/my-feature
gh pr create
```
