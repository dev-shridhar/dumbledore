#!/usr/bin/env python3
"""
PythonAnywhere entry point for Dumbledore bot.
This script can be run as a background task on PythonAnywhere.
"""
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from main import main

if __name__ == "__main__":
    main()
