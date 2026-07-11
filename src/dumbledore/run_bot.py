#!/usr/bin/env python3
from __future__ import annotations

import os

import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from dumbledore.main import main  # noqa: E402

if __name__ == "__main__":
    main()
