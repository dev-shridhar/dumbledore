# PythonAnywhere Deployment Guide

## Step 1: Upload Project

1. Go to [PythonAnywhere](https://www.pythonanywhere.com) → sign up / log in
2. Open **Dashboard** → **Files**
3. Upload the entire project folder, or use git:
   ```bash
   cd ~
   git clone https://github.com/dev-shridhar/dumbledore.git
   ```

## Step 2: Set Up Environment

1. Open **Bash console** from Dashboard
2. Run:
   ```bash
   cd ~/dumbledore
   pip3 install --user -r requirements.txt
   ```

## Step 3: Add Secrets

1. Go to **Dashboard** → **Tasks**
2. Or create `.env` file via Files:
   ```
   TELEGRAM_BOT_TOKEN=your_token
   GROQ_API_KEY=your_key
   OLLAMA_HOST= (leave empty, we'll use Groq only)
   ```

## Step 4: Run as Always-On Task

1. Go to **Dashboard** → **Tasks**
2. Click **Add a new task**
3. Set the command:
   ```
   /home/yourusername/.local/bin/python3 /home/yourusername/dumbledore/start_bot.py
   ```
4. Click **Run**

The bot will now run 24/7 on PythonAnywhere's free tier.

## Step 5: Verify

- Check **Tasks** page — your task should show as "Running"
- Go to Telegram → send `/start` to [@dumbledore_arch_bot](https://t.me/dumbledore_arch_bot)

## Troubleshooting

- If task stops: check **Logs** tab on Tasks page
- If import errors: make sure you ran `pip3 install --user -r requirements.txt`
- If token errors: verify `.env` file has correct values

## Updating the Bot

1. Upload new files via Files page, or
2. In Bash console:
   ```bash
   cd ~/dumbledore
   git pull
   ```
3. Restart the task from Tasks page
