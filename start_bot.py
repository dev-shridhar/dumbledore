#!/usr/bin/env python3
"""Startup script for PythonAnywhere deployment."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from main import main  # noqa: E402

if __name__ == "__main__":
    main()
