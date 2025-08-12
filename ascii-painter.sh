#!/bin/bash

# ASCII Painter - Slack-Optimized ASCII Art Generator
# This script runs the ascii-painter tool using uv from any directory

# Get the directory where this script is located (project root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Save current directory to return to it later
ORIGINAL_DIR="$(pwd)"

# Change to the project directory to run uv
cd "$SCRIPT_DIR"

# Run the ascii-painter using uv, but handle file paths relative to original directory
if [ $# -gt 0 ] && [ "${1:0:1}" != "-" ] && [ -f "$ORIGINAL_DIR/$1" ]; then
    # First argument is a file path, make it absolute
    FIRST_ARG="$ORIGINAL_DIR/$1"
    shift
    uv run ascii-painter "$FIRST_ARG" "$@"
else
    # No file path or file doesn't exist in original dir, pass arguments as-is
    uv run ascii-painter "$@"
fi

# Return to original directory
cd "$ORIGINAL_DIR"
