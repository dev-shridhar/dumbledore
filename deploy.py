#!/usr/bin/env python3
"""
Deploy script for PythonAnywhere.
Usage: python deploy.py --token <PA_TOKEN> --user <PA_USER>
"""
import argparse
import os
import subprocess
import sys


def run_cmd(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def deploy(token: str, user: str) -> None:
    print(f"🚀 Deploying to PythonAnywhere as {user}...")

    # 1. Upload files
    print("\n📦 Uploading files...")
    run_cmd(f'pythonanywhere -token "{token}" -user "{user}" files upload . dumbledore')

    # 2. Install dependencies
    print("\n📥 Installing dependencies...")
    run_cmd(
        f'pythonanywhere -token "{token}" -user "{user}" '
        f'bash "{user}@ssh.pythonanywhere.com" '
        f'"pip3 install -r ~/dumbledore/requirements.txt --user"'
    )

    # 3. Create .env file with secrets
    print("\n🔐 Setting environment variables...")
    env_content = f"""TELEGRAM_BOT_TOKEN={os.getenv('TELEGRAM_BOT_TOKEN', '')}
GROQ_API_KEY={os.getenv('GROQ_API_KEY', '')}
BOT_USERNAME={os.getenv('BOT_USERNAME', '')}
"""
    # Write env file locally first
    with open(".env.deploy", "w") as f:
        f.write(env_content)

    # Upload .env file
    cmd = f'pythonanywhere -token "{token}" -user "{user}"'
    run_cmd(f'{cmd} files upload .env.deploy dumbledore/.env')
    os.remove(".env.deploy")

    # 4. Kill existing bot process
    print("\n🔄 Restarting bot...")
    run_cmd(
        f'pythonanywhere -token "{token}" -user "{user}" '
        f'bash "{user}@ssh.pythonanywhere.com" '
        f'"pkill -f \'python3.*run_bot.py\' || true"'
    )

    # 5. Start bot in background
    run_cmd(
        f'pythonanywhere -token "{token}" -user "{user}" '
        f'bash "{user}@ssh.pythonanywhere.com" '
        f'"cd ~/dumbledore && nohup python3 run_bot.py > ~/dumbledore/bot.log 2>&1 &"'
    )

    print("\n✅ Deployment complete!")
    print(f"📊 Check logs: pythonanywhere -token '{token}' -user '{user}' "
          f'bash "{user}@ssh.pythonanywhere.com" "cat ~/dumbledore/bot.log"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy to PythonAnywhere")
    parser.add_argument("--token", required=True, help="PythonAnywhere API token")
    parser.add_argument("--user", required=True, help="PythonAnywhere username")
    args = parser.parse_args()
    deploy(args.token, args.user)
