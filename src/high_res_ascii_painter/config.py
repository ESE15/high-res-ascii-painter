"""
Configuration constants for ASCII art generator
"""

# Slack-optimized density string
# Carefully selected characters that render well in Slack's code blocks
# Ordered from darkest to lightest, avoiding problematic Unicode characters
DENSITY_STRING = '@#%*+=:-. '  # Simple ASCII characters that work consistently in Slack

# Image enhancement settings
CONTRAST_FACTOR = 2.0  # Higher contrast for better definition in Slack (0.5 to 2.0, where 1.0 is normal)
BRIGHTNESS_OFFSET = 10  # Slightly brighter for better visibility (-50 to 50)

# ASCII conversion settings
ASPECT_RATIO_CORRECTION = 0.5  # Adjusted for Slack's monospace font characteristics
GAMMA_CORRECTION = 0.6  # Stronger correction for better contrast with limited characters

# Default values
DEFAULT_WIDTH = 70
DEFAULT_TIMEOUT = 15

# Web request headers
WEB_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
