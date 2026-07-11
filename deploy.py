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
import sys
import time

BASE_URL = "https://www.pythonanywhere.com/api/v0/user"


def api_call(
    user: str,
    token: str,
    endpoint: str,
    method: str = "GET",
    data: str | None = None,
    file_path: str | None = None,
) -> tuple[int, str]:
    url = f"{BASE_URL}/{user}/{endpoint}"
    cmd = ["curl", "-s", "-w", "\nHTTP_CODE:%{http_code}", "-X", method, url,
           "-H", f"Authorization: Token {token}"]
    if file_path:
        cmd.extend(["-F", f"content=@{file_path}"])
    elif data:
        cmd.extend(["-H", "Content-Type: application/json", "-d", data])
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    http_code = output.split("HTTP_CODE:")[-1].strip() if "HTTP_CODE:" in output else "000"
    body = output.rsplit("HTTP_CODE:", 1)[0].strip()
    return int(http_code), body


def run_console_command(user: str, token: str, console_id: int, command: str) -> str:
    url = f"{BASE_URL}/{user}/consoles/{console_id}/send_input/"
    subprocess.run(
        ["curl", "-s", "-X", "POST", url,
         "-H", f"Authorization: Token {token}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({"input": command + "\n"})],
        capture_output=True,
    )
    time.sleep(3)
    out_url = f"{BASE_URL}/{user}/consoles/{console_id}/get_latest_output/"
    result = subprocess.run(
        ["curl", "-s", out_url, "-H", f"Authorization: Token {token}"],
        capture_output=True, text=True,
    )
    return result.stdout


def deploy(token: str, user: str) -> None:
    print(f"Deploying to PythonAnywhere as {user}...")

    # 0. Test connection
    print("\nTesting API connection...")
    code, body = api_call(user, token, "cpu/")
    if code != 200:
        print(f"ERROR: API connection failed (HTTP {code})")
        print(f"Response: {body}")
        print("Check PA_TOKEN and PA_USER secrets.")
        sys.exit(1)
    print("API connection OK")

    # 1. Upload files
    print("\nUploading files...")
    uploaded = 0
    for root, _dirs, files in os.walk("."):
        if ".git" in root or ".github" in root or "__pycache__" in root:
            continue
        for fname in files:
            if fname.endswith((".pyc",)) or fname == ".DS_Store":
                continue
            local_path = os.path.join(root, fname)
            remote_path = f"/home/{user}/dumbledore/{os.path.relpath(local_path, '.')}"
            code, _ = api_call(user, token, f"files/path{remote_path}",
                               method="POST", file_path=local_path)
            status = "OK" if code in (200, 201) else f"FAIL ({code})"
            print(f"  {local_path} -> {remote_path} [{status}]")
            uploaded += 1
    print(f"Uploaded {uploaded} files")

    # 2. Create console
    print("\nCreating console...")
    code, body = api_call(user, token, "consoles/",
                          method="POST", data=json.dumps({"executable": "bash"}))
    if code != 201:
        print(f"ERROR: Failed to create console (HTTP {code}): {body}")
        sys.exit(1)
    console_id = json.loads(body)["id"]
    print(f"Console ID: {console_id}")

    try:
        # 3. Install dependencies
        print("\nInstalling dependencies...")
        output = run_console_command(
            user, token, console_id,
            f"pip3 install -r /home/{user}/dumbledore/requirements.txt --user",
        )
        print(output[:500])

        # 4. Create .env
        print("\nCreating .env file...")
        env_content = (
            f"TELEGRAM_BOT_TOKEN={os.getenv('TELEGRAM_BOT_TOKEN', '')}\n"
            f"GROQ_API_KEY={os.getenv('GROQ_API_KEY', '')}\n"
            f"BOT_USERNAME={os.getenv('BOT_USERNAME', '')}"
        )
        escaped = env_content.replace("'", "'\\''")
        run_console_command(
            user, token, console_id,
            f"cat > /home/{user}/dumbledore/.env << 'ENVEOF'\n{escaped}\nENVEOF",
        )

        # 5. Restart bot
        print("\nRestarting bot...")
        run_console_command(user, token, console_id, "pkill -f run_bot.py || true")
        output = run_console_command(
            user, token, console_id,
            f"cd /home/{user}/dumbledore && nohup python3 run_bot.py > bot.log 2>&1 &",
        )
        print(output[:500])
    finally:
        # Cleanup console
        api_call(user, token, f"consoles/{console_id}/", method="DELETE")

    print("\nDeployment complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy to PythonAnywhere")
    parser.add_argument("--token", required=True, help="PythonAnywhere API token")
    parser.add_argument("--user", required=True, help="PythonAnywhere username")
    args = parser.parse_args()
    deploy(args.token, args.user)
