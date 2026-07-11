#!/usr/bin/env python3
"""
Deploy script for PythonAnywhere using their REST API.
Usage: python deploy.py --token <PA_TOKEN> --user <PA_USER>
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess


def api_call(user: str, token: str, endpoint: str, method: str = "GET",
             data: str | None = None, content_type: str = "application/json") -> str:
    url = f"https://www.pythonanywhere.com/api/v0/user/{user}/{endpoint}"
    cmd = ["curl", "-s", "-X", method, url, "-H", f"Authorization: Token {token}"]
    if data:
        cmd.extend(["-H", f"Content-Type: {content_type}", "-d", data])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def deploy(token: str, user: str) -> None:
    print(f"🚀 Deploying to PythonAnywhere as {user}...")

    # 1. Upload files via tar
    print("\n📦 Uploading files...")
    subprocess.run(
        "find . -type f -not -path './.git/*' -not -path './.github/*' "
        "-not -name '.DS_Store' -exec cp --parents {} /tmp/pa_upload/ \\;",
        shell=True, check=True,
    )
    subprocess.run(
        "tar czf /tmp/dumbledore.tar.gz .",
        shell=True, cwd="/tmp/pa_upload", check=True,
    )
    with open("/tmp/dumbledore.tar.gz", "rb") as f:
        api_call(user, token, "files/path/~/",
                 method="POST", data=f.read(), content_type="application/gzip")

    # 2. Install dependencies
    print("\n📥 Installing dependencies...")
    api_call(user, token, "bash/",
             data=json.dumps({"command": "pip3 install -r ~/dumbledore/requirements.txt --user"}))

    # 3. Create .env file
    print("\n🔐 Setting environment variables...")
    env_content = (
        f"TELEGRAM_BOT_TOKEN={os.getenv('TELEGRAM_BOT_TOKEN', '')}\n"
        f"GROQ_API_KEY={os.getenv('GROQ_API_KEY', '')}\n"
        f"BOT_USERNAME={os.getenv('BOT_USERNAME', '')}\n"
    )
    escaped_env = env_content.replace("'", "'\\''")
    cmd = f"cat > ~/dumbledore/.env << 'ENVEOF'\n{escaped_env}ENVEOF"
    api_call(user, token, "bash/", data=json.dumps({"command": cmd}))

    # 4. Kill existing process
    print("\n🔄 Restarting bot...")
    api_call(user, token, "bash/",
             data=json.dumps({"command": "pkill -f run_bot.py || true"}))

    # 5. Start bot
    api_call(user, token, "bash/",
             data=json.dumps({"command": "cd ~/dumbledore && nohup python3 run_bot.py > ~/dumbledore/bot.log 2>&1 &"}))

    print("\n✅ Deployment complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy to PythonAnywhere")
    parser.add_argument("--token", required=True, help="PythonAnywhere API token")
    parser.add_argument("--user", required=True, help="PythonAnywhere username")
    args = parser.parse_args()
    deploy(args.token, args.user)
