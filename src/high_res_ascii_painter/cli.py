"""
Command line interface for ASCII art generator
"""

import sys
from .config import DEFAULT_WIDTH


def print_help():
    """Print help message"""
    print("Slack-Optimized ASCII Art Generator")
    print("Usage: python painter.py <image_file> [width] [options]")
    print("       python painter.py -w <image_url> [width] [options]")
    print("       python painter.py --clip [width] [options]")
    print()
    print("Arguments:")
    print("  image_file    Path to the input image file")
    print("  image_url     URL to an image (use with -w option)")
    print("  width         ASCII art width in characters (default: 70)")
    print()
    print("Options:")
    print("  -w, --web     Download image from URL instead of local file")
    print("  --clip, -v    Use image from clipboard (requires WSL/PowerShell)")
    print("  -a, --auto-copy  Copy ASCII art result to clipboard automatically")
    print("  --color, -c   Enable colored output (not recommended for Slack)")
    print("  --trim, -t    Remove background-only rows and columns for compact output")
    print("  --help, -h    Show this help message")
    print()
    print("Slack Usage Tips:")
    print("  - Use width 60-80 for best results in Slack code blocks")
    print("  - Copy output and paste into Slack using code block (```)")
    print("  - Avoid color mode when pasting to Slack")
    print()
    print("Web Image Notes:")
    print("  - Slack file URLs require authentication and won't work directly")
    print("  - Use public image hosting services (imgur, picsum.photos, etc.)")
    print("  - Some websites may block automated requests")
    print()
    print("Clipboard Notes:")
    print("  - Requires WSL/Windows environment with PowerShell")
    print("  - Copy an image to clipboard before running with --clip")
    print("  - Auto-copy (-a) removes color codes for better compatibility")
    print("  - Temporary files are automatically cleaned up")
    print()
    print("Examples:")
    print("  python painter.py image.jpg 70")
    print("  python painter.py -w https://picsum.photos/400/300 60")
    print("  python painter.py --clip 80 --trim")
    print("  python painter.py image.jpg 70 -a --trim")
    print("  python painter.py --web https://imgur.com/image.jpg --trim")
    print("  python painter.py image.jpg 80 --trim --color")


class ArgumentParser:
    """Parse command line arguments"""
    
    def __init__(self):
        self.use_web = False
        self.use_clipboard = False
        self.auto_copy = False
        self.use_color = False
        self.use_trim = False
        self.img_source = None
        self.width = DEFAULT_WIDTH
    
    def parse_args(self, argv):
        """Parse command line arguments"""
        # Check for help
        if len(argv) < 2 or '--help' in argv or '-h' in argv:
            print_help()
            sys.exit(0)
        
        # Parse flags
        self.use_web = '--web' in argv or '-w' in argv
        self.use_clipboard = '--clip' in argv or '-v' in argv
        self.auto_copy = '--auto-copy' in argv or '-a' in argv
        self.use_color = '--color' in argv or '-c' in argv
        self.use_trim = '--trim' in argv or '-t' in argv
        
        # Remove flags from argv to get positional arguments
        filtered_argv = [arg for arg in argv if not arg.startswith('-')]
        
        if self.use_clipboard:
            # For clipboard mode, no image source needed, just optional width
            self.img_source = None  # Will be handled by clipboard function
            try:
                self.width = int(filtered_argv[1]) if len(filtered_argv) > 1 else DEFAULT_WIDTH
            except (IndexError, ValueError):
                self.width = DEFAULT_WIDTH
        elif self.use_web:
            # For web mode, expect URL as first argument after script name
            if len(filtered_argv) < 2:
                print("Error: URL required when using -w/--web option")
                sys.exit(1)
            self.img_source = filtered_argv[1]
            try:
                self.width = int(filtered_argv[2]) if len(filtered_argv) > 2 else DEFAULT_WIDTH
            except (IndexError, ValueError):
                self.width = DEFAULT_WIDTH
        else:
            # For file mode, expect filename as first argument
            if len(filtered_argv) < 2:
                print("Error: Image file required")
                sys.exit(1)
            self.img_source = filtered_argv[1]
            try:
                self.width = int(filtered_argv[2]) if len(filtered_argv) > 2 else DEFAULT_WIDTH
            except (IndexError, ValueError):
                self.width = DEFAULT_WIDTH
        
        return self
