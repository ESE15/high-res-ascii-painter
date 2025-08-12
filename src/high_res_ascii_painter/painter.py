#!/usr/bin/env python3
"""
Slack-Optimized ASCII Art Generator

A modular ASCII art generator optimized for Slack code blocks.
Supports both local files and web URLs with various customization options.
"""

import sys
from .cli import ArgumentParser
from .image_loader import load_image
from .ascii_converter import ASCIIConverter
from .utils import trim_ascii_art


def main():
    """Main entry point for the ASCII art generator"""
    # Parse command line arguments
    parser = ArgumentParser()
    args = parser.parse_args(sys.argv)
    
    # Load the image
    img = load_image(args.img_source, args.use_web)
    
    # Create ASCII converter with color support if requested
    converter = ASCIIConverter(use_color=args.use_color)
    
    # Convert image to ASCII art
    ascii_lines = converter.convert_to_ascii(img, args.width)
    
    # Apply trimming if requested
    if args.use_trim:
        ascii_lines = trim_ascii_art(ascii_lines)
    
    # Output the final result
    for line in ascii_lines:
        print(line)


if __name__ == "__main__":
    main()