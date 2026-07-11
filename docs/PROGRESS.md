# Dumbledore — Progress Board

Track what's done, in progress, and what's next. Tag format: `[status] category: description`

---

## ✅ Done

### Features
- [x] `main.py` — Telegram bot with challenge, ask, conclude, clear, status, prompts handlers
- [x] `brain.py` — Versioned prompt loader and message builder
- [x] `llm.py` — Ollama primary + Groq fallback chat client
- [x] `memory.py` — Per-group chat history buffer (GroupMemory class)
- [x] `config.py` — .env loading with Config dataclass
- [x] Prompts v1.0.0 — `challenge_v1.py`, `ask_v1.py`, `conclude_v1.py`
- [x] Bot responds in group chats when replied to
- [x] `/ask`, `/conclude`, `/clear`, `/status`, `/prompts` commands working
- [x] Groq fallback confirmed working locally

### Bug Fixes
- [x] Spelling fixed: dumbeldore → dumbledore everywhere
- [x] Telegram token revoked and regenerated (old one compromised)
- [x] Branch protection check names fixed to match CI matrix (`Tests / tests (3.10)` etc.)

### CI/CD
- [x] GitHub Actions workflow: ruff → mypy → pytest on Python 3.10, 3.11, 3.12
- [x] 20 tests passing across all 3 Python versions
- [x] GitHub Secrets configured: `TELEGRAM_BOT_TOKEN`, `GROQ_API_KEY`

### Docs
- [x] `README.md` — Project overview
- [x] `DEPLOY.md` — PythonAnywhere deployment guide
- [x] `AGENTS.md` — Developer guide with all rules and conventions
- [x] `PROGRESS.md` — This file

### Infrastructure
- [x] GitHub repo created and renamed to `dumbledore`
- [x] bhargavhasabnis invited as admin collaborator
- [x] `start_bot.py` — Entry point that loads .env

---

## 🔄 In Progress

### Deployment
- [ ] Decide on hosting platform
- [ ] Deploy bot and verify it responds in Telegram

---

## 📋 To Do

### Features
- [ ] Add rate limiting per group (prevent spam)
- [ ] Add `/help` with detailed usage instructions per command
- [ ] Add error handling for Groq API failures (retry, fallback message)
- [ ] Add typing indicators while bot generates response
- [ ] Support reply chains (track which message is being replied to)
- [ ] Add conversation persistence (currently in-memory only, lost on restart)

### Security
- [ ] Rotate Telegram token (was shared in chat)
- [ ] Rotate Groq API key (was shared in chat)
- [ ] Create `.env.example` with placeholder values

### CI/CD
- [ ] Add test coverage reporting (pytest-cov)
- [ ] Add dependency scanning (Dependabot or Renovate)
- [ ] Add Dockerfile for containerized deployment

### Docs
- [ ] Add architecture diagram
- [ ] Add API documentation for LLM fallback chain
- [ ] Add troubleshooting guide

### Enhancements
- [ ] Support private chats (not just groups)
- [ ] Add custom prompt per group (admin command)
- [ ] Add usage analytics (how many challenges, asks, etc.)
- [ ] Add webhook support for faster response (instead of polling)

---

## 🐛 Bugs

_No known bugs at this time._

---

## 📝 Notes

- **Telegram bot:** @dumbledore_arch_bot
- **Owner GitHub:** dev-shridhar
- **Collaborator:** bhargavhasabnis (admin)
- **LLM:** Groq API working, Ollama not set up locally yet

---

## 🔗 Links

- Repo: https://github.com/dev-shridhar/dumbledore
- Telegram Bot: https://t.me/dumbledore_arch_bot
- PythonAnywhere: https://www.pythonanywhere.com/account/
