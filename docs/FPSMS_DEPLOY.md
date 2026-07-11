# FPS.ms Deployment Guide

## Overview

This guide covers deploying Dumbledore to FPS.ms, a free Telegram bot hosting platform.

**Platform:** FPS.ms
**Cost:** Free (24-hour renewal required)
**Resources:** 25% CPU, 128 MB RAM, 250 MB storage
**URL:** https://fps.ms

## Prerequisites

1. **FPS.ms Account** - Sign up at https://panel.fps.ms
2. **Telegram Bot Token** - From @BotFather
3. **Groq API Key** - From https://console.groq.com

## Step 1: Prepare Your Files

You'll need to upload these files to FPS.ms:

```
dumbledore/
├── app.py                    # Entry point (created for FPS.ms)
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create from .env.example)
└── src/                      # Source code directory
    ├── brain.py
    ├── config.py
    ├── llm.py
    ├── main.py
    ├── memory.py
    └── prompts/
        ├── __init__.py
        ├── ask_v1.py
        ├── challenge_v1.py
        └── conclude_v1.py
```

## Step 2: Create .env File

Create a `.env` file with your credentials:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
BOT_USERNAME=your_bot_username
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
OLLAMA_HOST=
OLLAMA_MODEL=llama3.1:8b
LLM_TIMEOUT=30
MAX_HISTORY=50
CONTEXT_MESSAGES=20
ADMIN_USER_IDS=
```

**Important:** Never commit `.env` to git. It's already in `.gitignore`.

## Step 3: Upload to FPS.ms

### Option A: Panel File Manager

1. Log in to https://panel.fps.ms
2. Create a new server (select Python/Telegram bot package)
3. Go to **Files** tab
4. Upload all files maintaining the directory structure:
   - Upload `app.py` to root
   - Upload `requirements.txt` to root
   - Upload `.env` to root
   - Upload entire `src/` directory

### Option B: SFTP

1. Get SFTP credentials from FPS.ms panel
2. Connect via SFTP client (FileZilla, Cyberduck, etc.)
3. Upload all files maintaining directory structure

### Option C: Git Repository

1. Push code to GitHub/GitLab
2. In FPS.ms panel, go to **Startup** tab
3. Enter your Git repo URL
4. Click **Reinstall Server**

## Step 4: Configure Startup

1. In FPS.ms panel, go to **Startup** tab
2. Set **Startup Command** to:
   ```
   python3 app.py
   ```
3. Ensure **Python packages** includes:
   ```
   python-telegram-bot==21.3
   openai==1.45.0
   httpx==0.27.2
   python-dotenv==1.0.1
   ```

## Step 5: Start the Bot

1. Go to **Console** tab
2. Click **Start**
3. You should see: `Dumbledore starting...`
4. Test in Telegram by sending `/start` to your bot

## Step 6: Daily Renewal

**Important:** FPS.ms free tier requires renewal every 24 hours.

### Manual Renewal
1. Log in to FPS.ms panel daily
2. Click **Renew** to keep bot online

### Automated Renewal (Optional)
If FPS.ms provides an API, you can set up automated renewal:

```bash
# Example cron job (runs every 23 hours)
0 */23 * * * curl -X POST "https://api.fps.ms/renew/YOUR_SERVER_ID" -H "Authorization: Bearer YOUR_TOKEN"
```

Check FPS.ms documentation for API availability.

## Troubleshooting

### Bot Won't Start

**Error:** `No such file or directory: app.py`
- **Solution:** Ensure `app.py` is in the root directory

**Error:** `ModuleNotFoundError`
- **Solution:** Check `requirements.txt` has all dependencies

**Error:** `TELEGRAM_BOT_TOKEN not set`
- **Solution:** Verify `.env` file exists and has correct token

### Bot Starts But Doesn't Respond

1. Check console for error messages
2. Verify bot token is correct
3. Ensure bot is added to a group
4. Check if bot has proper permissions

### Bot Stops After 24 Hours

- This is expected behavior for free tier
- Renew manually or set up automated renewal

## Differences from PythonAnywhere

| Feature | FPS.ms | PythonAnywhere |
|---------|--------|----------------|
| **Free Tier** | Yes (24h renewal) | Yes (limited) |
| **Always-On** | No (requires renewal) | Paid only ($10/mo) |
| **Entry Point** | `app.py` | `start_bot.py` |
| **Dependencies** | Auto-installed | Manual `pip install` |
| **SFTP Access** | Yes | Yes |
| **Public URL** | No (free tier) | Yes (web app) |

## File Structure for FPS.ms

```
/app.py              <- Entry point (FPS.ms runs this)
/requirements.txt    <- Dependencies (auto-installed)
/.env                <- Secrets (never commit)
/src/
  /brain.py
  /config.py
  /llm.py
  /main.py
  /memory.py
  /prompts/
    /__init__.py
    /ask_v1.py
    /challenge_v1.py
    /conclude_v1.py
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | From @BotFather |
| `BOT_USERNAME` | Yes | Bot username without @ |
| `GROQ_API_KEY` | Yes | From console.groq.com |
| `GROQ_MODEL` | No | Default: llama-3.1-8b-instant |
| `OLLAMA_HOST` | No | Leave empty for FPS.ms |
| `OLLAMA_MODEL` | No | Default: llama3.1:8b |
| `LLM_TIMEOUT` | No | Default: 30 seconds |
| `MAX_HISTORY` | No | Default: 50 messages |
| `CONTEXT_MESSAGES` | No | Default: 20 messages |
| `ADMIN_USER_IDS` | No | Comma-separated user IDs |

## Next Steps

1. Deploy to FPS.ms using this guide
2. Test bot in Telegram
3. Set up daily renewal (manual or automated)
4. Monitor bot performance in FPS.ms console

## Support

- **FPS.ms Docs:** https://docs.fps.ms
- **FPS.ms Discord:** https://fps.ms/discord
- **Dumbledore Repo:** https://github.com/dev-shridhar/dumbledore
