# Dumbledore

Socratic AI bot for Telegram — challenges your thinking on system design, DSA & architecture.

> *"It is our choices, Harry, that show what we truly are, far more than our abilities."*
> — Albus Dumbledore

## Features

- **Challenge mode**: Reply to any message in a group and the bot probes your thinking with Socratic questions
- **Ask mode**: `/ask <question>` for deep expert answers
- **Conclude mode**: `/conclude` to wrap up discussions with the correct answer
- **Prompt versioning**: Each mode has its own versioned prompt — easy to A/B test and iterate

## How It Works

```
Group conversation happening
        │
        ├─ Reply to message → CHALLENGE (Socratic mode)
        │   "Why X? What about Y? Trade-offs?"
        │
        ├─ /ask <question> → ASK (expert mode)
        │   Deep, authoritative response
        │
        └─ /conclude → CONCLUDE (summary mode)
            "Here's what we discussed...
             Points X and Y were valid...
             The best approach is Z because..."
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with usage guide |
| `/ask <question>` | Get a deep expert answer |
| `/conclude` | Summarize discussion with the correct answer |
| `/clear` | Reset bot memory for this group |
| `/status` | Show buffer count, prompt version, model |
| `/prompts` | Show current prompt versions |

## Setup

1. Clone the repo
   ```bash
    git clone https://github.com/dev-shridhar/dumbledore.git
   cd dumbledore
   ```

2. Create your `.env` file
   ```bash
   cp .env.example .env
   ```
   Fill in:
   - `TELEGRAM_BOT_TOKEN` — from [@BotFather](https://t.me/BotFather)
   - `GROQ_API_KEY` — from [console.groq.com](https://console.groq.com)
   - Optionally set `OLLAMA_HOST` for local models

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run
   ```bash
   python main.py
   ```

## LLM Backend

- **Primary**: Ollama (local) — set `OLLAMA_HOST` and `OLLAMA_MODEL`
- **Fallback**: Groq API — free tier, fast inference
- Bot automatically falls back to Groq if Ollama is unavailable

## Prompt Versioning

Prompts live in `prompts/` as versioned files:
```
prompts/
├── __init__.py          # VERSION = "1.0.0"
├── challenge_v1.py      # Socratic questioning prompt
├── ask_v1.py            # Expert answer prompt
└── conclude_v1.py       # Discussion summary prompt
```

To update a prompt: create a new version file (e.g., `challenge_v2.py`) and update the imports in `brain.py`.

## Project Structure

```
dumbledore/
├── main.py              # Telegram handlers
├── brain.py             # Versioned prompt loader
├── llm.py               # Ollama + Groq fallback
├── memory.py            # Per-group chat history
├── config.py            # .env configuration
├── prompts/             # Versioned prompt files
├── tests/               # 20 tests
└── .github/workflows/   # CI/CD pipeline
```

## Development

```bash
# Run tests
pytest tests/ -v

# Lint
ruff check .

# Type check
mypy --ignore-missing-imports .
```

**Workflow**: Never commit directly to `main`. Create a feature branch, open a PR, and merge only after CI passes.

## License

MIT
