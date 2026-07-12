#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import dotenv

dotenv.load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from main import main  # noqa: E402

if __name__ == "__main__":
    main()
