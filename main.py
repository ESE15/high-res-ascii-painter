#!/usr/bin/env python3
"""
ASCII Painter - Main entry point for PyInstaller
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main function
from high_res_ascii_painter.painter import main

if __name__ == "__main__":
    main()
