from __future__ import annotations

from prompts import VERSION
from prompts.ask_v1 import ASK_PROMPT_V1
from prompts.challenge_v3 import CHALLENGE_PROMPT_V3
from prompts.conclude_v1 import CONCLUDE_PROMPT_V1
from prompts.learn_v1 import LEARN_PROMPT_V1

PROMPTS = {
    "challenge": CHALLENGE_PROMPT_V3,
    "ask": ASK_PROMPT_V1,
    "conclude": CONCLUDE_PROMPT_V1,
    "learn": LEARN_PROMPT_V1,
}


def get_system_prompt(mode: str) -> str:
    prompt = PROMPTS.get(mode)
    if not prompt:
        raise ValueError(f"Unknown mode: {mode}. Available: {list(PROMPTS.keys())}")
    return prompt


def build_messages(mode: str, context: list[dict], user_query: str | None = None) -> list[dict]:
    system_prompt = get_system_prompt(mode)
    messages = [{"role": "system", "content": system_prompt}]

    if context:
        context_text = "\n".join(
            f"{msg.get('sender', 'Unknown')}: {msg['text']}" for msg in context
        )
        messages.append({
            "role": "user",
            "content": f"Here is the group conversation context:\n\n{context_text}",
        })

    if user_query:
        messages.append({"role": "user", "content": user_query})

    return messages


def get_prompt_version() -> str:
    return VERSION
