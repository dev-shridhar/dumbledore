from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI

from dumbledore.config import config

logger = logging.getLogger(__name__)


def _ollama_chat(messages: list[dict[str, Any]]) -> str | None:
    try:
        client = OpenAI(
            base_url=f"{config.ollama_host}/v1",
            api_key="ollama",
        )
        response = client.chat.completions.create(
            model=config.ollama_model,
            messages=messages,  # type: ignore[arg-type]
            timeout=config.llm_timeout,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.warning(f"Ollama failed: {e}")
        return None


def _groq_chat(messages: list[dict[str, Any]]) -> str | None:
    if not config.groq_api_key:
        logger.warning("No Groq API key configured")
        return None
    try:
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=config.groq_api_key,
        )
        response = client.chat.completions.create(
            model=config.groq_model,
            messages=messages,  # type: ignore[arg-type]
            timeout=config.llm_timeout,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.warning(f"Groq failed: {e}")
        return None


def chat(messages: list[dict[str, Any]]) -> str:
    result = _ollama_chat(messages)
    if result:
        return result

    logger.info("Falling back to Groq...")
    result = _groq_chat(messages)
    if result:
        return result

    return "Sorry, both Ollama and Groq are unavailable right now. Please try again later."
