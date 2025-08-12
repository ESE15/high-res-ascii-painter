#!/usr/bin/env python3
"""
Slack-Optimized ASCII Art Generator

A modular ASCII art generator optimized for Slack code blocks.
Supports both local files and web URLs with various customization options.
"""

import sys
import os
from .cli import ArgumentParser
from .image_loader import load_image
from .ascii_converter import ASCIIConverter
from .utils import trim_ascii_art, save_clipboard_image


def main():
    """Main entry point for the ASCII art generator"""
    # Parse command line arguments
    parser = ArgumentParser()
    args = parser.parse_args(sys.argv)
    
    # Handle clipboard mode
    if args.use_clipboard:
        try:
            print("Getting image from clipboard...")
            temp_image_path = save_clipboard_image()
            img_source = temp_image_path
            use_web = False
        except RuntimeError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        img_source = args.img_source
        use_web = args.use_web
    
    try:
        # Load the image
        img = load_image(img_source, use_web)
        
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
            
    finally:
        # Clean up temporary file if we created one
        if args.use_clipboard and 'temp_image_path' in locals():
            try:
                os.unlink(temp_image_path)
                print(f"Temporary file cleaned up: {temp_image_path}")
            except OSError:
                pass  # File might already be deleted


if __name__ == "__main__":
    main()