import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

# Load .env file for local development
# On PythonAnywhere / GitHub Actions, set env vars directly
load_dotenv()


@dataclass
class Config:
    telegram_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    bot_username: str = field(default_factory=lambda: os.getenv("BOT_USERNAME", ""))

    ollama_host: str = field(default_factory=lambda: os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    ollama_model: str = field(default_factory=lambda: os.getenv("OLLAMA_MODEL", "llama3.1:8b"))

    groq_api_key: str = field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    groq_model: str = field(default_factory=lambda: os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"))

    llm_timeout: int = int(os.getenv("LLM_TIMEOUT", "30"))
    max_history: int = int(os.getenv("MAX_HISTORY", "50"))
    context_messages: int = int(os.getenv("CONTEXT_MESSAGES", "20"))

    admin_user_ids: list[int] = field(default_factory=lambda: [
        int(x.strip()) for x in os.getenv("ADMIN_USER_IDS", "").split(",") if x.strip()
    ])


config = Config()
