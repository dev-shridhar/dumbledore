from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from dumbledore.config import config


@dataclass
class ChatMessage:
    sender: str
    text: str
    message_id: int


class GroupMemory:
    def __init__(self, max_messages: int | None = None):
        self.max_messages = max_messages or config.max_history
        self._buffers: dict[int, list[ChatMessage]] = defaultdict(list)

    def add_message(self, chat_id: int, sender: str, text: str, message_id: int) -> None:
        msg = ChatMessage(sender=sender, text=text, message_id=message_id)
        self._buffers[chat_id].append(msg)
        if len(self._buffers[chat_id]) > self.max_messages:
            self._buffers[chat_id] = self._buffers[chat_id][-self.max_messages:]

    def get_context(self, chat_id: int, limit: int | None = None) -> list[dict]:
        n = limit or config.context_messages
        messages = self._buffers.get(chat_id, [])[-n:]
        return [{"sender": m.sender, "text": m.text} for m in messages]

    def clear(self, chat_id: int) -> None:
        self._buffers.pop(chat_id, None)

    def get_message_count(self, chat_id: int) -> int:
        return len(self._buffers.get(chat_id, []))


memory = GroupMemory()
