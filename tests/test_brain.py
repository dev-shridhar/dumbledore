from brain import build_messages, get_prompt_version, get_system_prompt


def test_get_prompt_version():
    version = get_prompt_version()
    assert version == "1.0.0"


def test_get_system_prompt_challenge():
    prompt = get_system_prompt("challenge")
    assert "Socratic" in prompt or "NEVER give the answer" in prompt


def test_get_system_prompt_ask():
    prompt = get_system_prompt("ask")
    assert "DEEP" in prompt or "comprehensive" in prompt


def test_get_system_prompt_conclude():
    prompt = get_system_prompt("conclude")
    assert "SUMMARY" in prompt or "conclude" in prompt.lower() or "Question" in prompt


def test_get_system_prompt_invalid():
    try:
        get_system_prompt("invalid")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown mode" in str(e)


def test_build_messages_challenge():
    context = [
        {"sender": "Alice", "text": "Use a hash map for O(1) lookup"},
        {"sender": "Bob", "text": "But what about collision handling?"},
    ]
    messages = build_messages("challenge", context, "Why a hash map?")
    assert messages[0]["role"] == "system"
    assert any("Alice" in m["content"] for m in messages if m["role"] == "user")
    assert messages[-1]["content"] == "Why a hash map?"


def test_build_messages_empty_context():
    messages = build_messages("ask", [], "What is a B-tree?")
    assert messages[0]["role"] == "system"
    assert messages[-1]["content"] == "What is a B-tree?"


def test_build_messages_with_user_query():
    messages = build_messages("conclude", [{"sender": "X", "text": "Use Redis"}], None)
    assert len(messages) == 2
    assert "Redis" in messages[1]["content"]
