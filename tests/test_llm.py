from unittest.mock import patch

from llm import _groq_chat, _ollama_chat, chat


def test_chat_fallback_to_groq():
    with patch("llm._ollama_chat", return_value=None), \
         patch("llm._groq_chat", return_value="Groq response"):
        result = chat([{"role": "user", "content": "hi"}])
        assert result == "Groq response"


def test_chat_ollama_primary():
    with patch("llm._ollama_chat", return_value="Ollama response"):
        result = chat([{"role": "user", "content": "hi"}])
        assert result == "Ollama response"


def test_chat_both_fail():
    with patch("llm._ollama_chat", return_value=None), \
         patch("llm._groq_chat", return_value=None):
        result = chat([{"role": "user", "content": "hi"}])
        assert "unavailable" in result.lower()


def test_ollama_chat_returns_none_on_error():
    with patch("llm.OpenAI", side_effect=Exception("connection refused")):
        result = _ollama_chat([{"role": "user", "content": "hi"}])
        assert result is None


def test_groq_chat_returns_none_without_key():
    with patch("llm.config") as mock_config:
        mock_config.groq_api_key = ""
        result = _groq_chat([{"role": "user", "content": "hi"}])
        assert result is None


def test_groq_chat_returns_none_on_error():
    with patch("llm.config") as mock_config, \
         patch("llm.OpenAI", side_effect=Exception("api error")):
        mock_config.groq_api_key = "test-key"
        result = _groq_chat([{"role": "user", "content": "hi"}])
        assert result is None
