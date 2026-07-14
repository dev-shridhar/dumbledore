# Prompt versions - each mode has its own versioned prompt file.
# To update a prompt: create a new version file and update VERSION in __init__.py

from prompts.ask_v1 import ASK_PROMPT_V1  # noqa: E402
from prompts.ask_v2 import ASK_PROMPT_V2  # noqa: E402
from prompts.challenge_v1 import CHALLENGE_PROMPT_V1  # noqa: E402
from prompts.challenge_v2 import CHALLENGE_PROMPT_V2  # noqa: E402
from prompts.challenge_v3 import CHALLENGE_PROMPT_V3  # noqa: E402
from prompts.conclude_v1 import CONCLUDE_PROMPT_V1  # noqa: E402
from prompts.conclude_v2 import CONCLUDE_PROMPT_V2  # noqa: E402
from prompts.learn_v1 import LEARN_PROMPT_V1  # noqa: E402

VERSION = "2.0.0"

PROMPT_MAP = {
    "ask": ASK_PROMPT_V2,
    "ask_v1": ASK_PROMPT_V1,
    "ask_v2": ASK_PROMPT_V2,
    "challenge": CHALLENGE_PROMPT_V3,
    "challenge_v1": CHALLENGE_PROMPT_V1,
    "challenge_v2": CHALLENGE_PROMPT_V2,
    "challenge_v3": CHALLENGE_PROMPT_V3,
    "conclude": CONCLUDE_PROMPT_V2,
    "conclude_v1": CONCLUDE_PROMPT_V1,
    "conclude_v2": CONCLUDE_PROMPT_V2,
    "learn": LEARN_PROMPT_V1,
    "learn_v1": LEARN_PROMPT_V1,
}
