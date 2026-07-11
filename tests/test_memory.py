from memory import GroupMemory


def test_add_and_get():
    mem = GroupMemory(max_messages=10)
    mem.add_message(1, "Alice", "Hello", 100)
    ctx = mem.get_context(1)
    assert len(ctx) == 1
    assert ctx[0]["sender"] == "Alice"
    assert ctx[0]["text"] == "Hello"


def test_max_messages_limit():
    mem = GroupMemory(max_messages=3)
    for i in range(5):
        mem.add_message(1, "User", f"msg-{i}", i)
    ctx = mem.get_context(1)
    assert len(ctx) == 3
    assert ctx[0]["text"] == "msg-2"


def test_clear():
    mem = GroupMemory()
    mem.add_message(1, "Alice", "Hi", 1)
    mem.clear(1)
    assert mem.get_context(1) == []


def test_separate_chats():
    mem = GroupMemory()
    mem.add_message(1, "Alice", "Hi", 1)
    mem.add_message(2, "Bob", "Hey", 2)
    assert len(mem.get_context(1)) == 1
    assert len(mem.get_context(2)) == 1
    assert mem.get_context(1)[0]["sender"] == "Alice"
    assert mem.get_context(2)[0]["sender"] == "Bob"


def test_message_count():
    mem = GroupMemory()
    assert mem.get_message_count(1) == 0
    mem.add_message(1, "A", "x", 1)
    assert mem.get_message_count(1) == 1


def test_context_limit():
    mem = GroupMemory(max_messages=100)
    for i in range(10):
        mem.add_message(1, "U", f"m-{i}", i)
    ctx = mem.get_context(1, limit=5)
    assert len(ctx) == 5
    assert ctx[0]["text"] == "m-5"
