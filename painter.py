import sys
import numpy as np
from PIL import Image, ImageEnhance
import requests
from io import BytesIO
import os

# Usage information
if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
    print("Slack-Optimized ASCII Art Generator")
    print("Usage: python painter_high_res_slack.py <image_file> [width] [options]")
    print("       python painter_high_res_slack.py -w <image_url> [width] [options]")
    print()
    print("Arguments:")
    print("  image_file    Path to the input image file")
    print("  image_url     URL to an image (use with -w option)")
    print("  width         ASCII art width in characters (default: 70)")
    print()
    print("Options:")
    print("  -w, --web     Download image from URL instead of local file")
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
    print("Examples:")
    print("  python painter_high_res_slack.py image.jpg 70")
    print("  python painter_high_res_slack.py -w https://picsum.photos/400/300 60")
    print("  python painter_high_res_slack.py --web https://imgur.com/image.jpg --trim")
    print("  python painter_high_res_slack.py image.jpg 80 --trim --color")
    sys.exit(0)

# ANSI color codes for colored output
def get_ansi_color(r, g, b):
    """Convert RGB to ANSI 256-color code"""
    return f'\033[38;2;{r};{g};{b}m'

def reset_color():
    """Reset to default color"""
    return '\033[0m'

def trim_ascii_art(ascii_lines):
    """Remove background rows and columns from ASCII art for compact output"""
    if not ascii_lines:
        return ascii_lines
    
    # Convert to list if it's a generator
    lines = list(ascii_lines)
    if not lines:
        return lines
    
    # Find background characters (lightest characters in our density string)
    # Include both space and the second-to-last character (which is usually '.')
    background_chars = set()
    if density:
        background_chars.add(density[-1])  # Last character (space)
        if len(density) > 1:
            background_chars.add(density[-2])  # Second to last character ('.')
    else:
        background_chars = {' ', '.'}
    
    # Debug: print background characters
    print(f"Debug: Background characters detected: {background_chars}")
    print(f"Debug: Density string: '{density}'")
    
    def is_background_only(text):
        """Check if text contains only background characters"""
        return all(char in background_chars for char in text.strip())
    
    # Remove background-only rows from top and bottom
    # Find first non-background row
    start_row = 0
    for i, line in enumerate(lines):
        if not is_background_only(line):
            start_row = i
            break
    else:
        # All lines are background only
        return []
    
    # Find last non-background row
    end_row = len(lines) - 1
    for i in range(len(lines) - 1, -1, -1):
        if not is_background_only(lines[i]):
            end_row = i
            break
    
    # Trim rows
    trimmed_lines = lines[start_row:end_row + 1]
    
    if not trimmed_lines:
        return []
    
    # Remove background-only columns from left and right
    max_width = max(len(line) for line in trimmed_lines)
    
    # Find first non-background column
    start_col = max_width
    for j in range(max_width):
        column_chars = []
        for line in trimmed_lines:
            if j < len(line):
                column_chars.append(line[j])
        
        # Check if this column has any non-background characters
        if any(char not in background_chars for char in column_chars):
            start_col = j
            break
    
    # Find last non-background column
    end_col = -1
    for j in range(max_width - 1, -1, -1):
        column_chars = []
        for line in trimmed_lines:
            if j < len(line):
                column_chars.append(line[j])
        
        # Check if this column has any non-background characters
        if any(char not in background_chars for char in column_chars):
            end_col = j
            break
    
    # If no non-background characters found
    if start_col >= max_width or end_col < 0:
        return []
    
    # Trim columns
    result = []
    for line in trimmed_lines:
        if end_col + 1 <= len(line):
            trimmed_line = line[start_col:end_col + 1]
        else:
            # Handle lines shorter than end_col
            if start_col < len(line):
                trimmed_line = line[start_col:]
            else:
                trimmed_line = ""
        
        # Remove trailing background characters
        while trimmed_line and trimmed_line[-1] in background_chars:
            trimmed_line = trimmed_line[:-1]
        
        result.append(trimmed_line)
    
    return result

def download_image_from_url(url):
    """Download image from URL and return PIL Image object"""
    try:
        print(f"Downloading image from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Special handling for known problematic domains
        if 'slack.com' in url:
            print("Warning: Slack files require authentication and may not be accessible directly.")
            print("Consider downloading the image manually and using a local file instead.")
            print("Alternative: Use a public image hosting service like imgur, picsum.photos, etc.")
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        # Check if the content is an image
        content_type = response.headers.get('content-type', '').lower()
        
        # More flexible content type checking
        if not (content_type.startswith('image/') or 
                any(img_type in content_type for img_type in ['jpeg', 'jpg', 'png', 'gif', 'webp', 'bmp'])):
            
            # Special message for HTML responses (common with authentication-required URLs)
            if 'text/html' in content_type:
                raise ValueError(f"URL returned HTML instead of an image. This usually means:\n"
                               f"  - The URL requires authentication (like Slack files)\n"
                               f"  - The URL is not a direct link to an image\n"
                               f"  - The server is blocking automated requests\n"
                               f"Content-Type: {content_type}")
            else:
                raise ValueError(f"URL does not point to an image. Content-Type: {content_type}")
        
        # Try to load image from bytes
        image_bytes = BytesIO(response.content)
        img = Image.open(image_bytes)
        print(f"Successfully downloaded image: {img.size[0]}x{img.size[1]} pixels")
        return img
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        if 'slack.com' in url:
            print("\nTip: Slack file URLs require authentication. Try:")
            print("  1. Download the image manually and use local file")
            print("  2. Upload image to a public service (imgur, etc.)")
            print("  3. Use a different public image URL for testing")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)

# Slack-optimized density string
# Carefully selected characters that render well in Slack's code blocks
# Ordered from darkest to lightest, avoiding problematic Unicode characters
density = ('@#%*+=:-. ')  # Simple ASCII characters that work consistently in Slack

# Contrast adjustment optimized for Slack visibility (0.5 to 2.0, where 1.0 is normal)
contrast_factor = 2.0  # Higher contrast for better definition in Slack
# Brightness adjustment (-50 to 50)
brightness_offset = 10  # Slightly brighter for better visibility

n = len(density)

# Parse command line arguments
use_web = '--web' in sys.argv or '-w' in sys.argv
use_color = '--color' in sys.argv or '-c' in sys.argv
use_trim = '--trim' in sys.argv or '-t' in sys.argv

# Remove flags from argv to get positional arguments
filtered_argv = [arg for arg in sys.argv if not arg.startswith('-')]

if use_web:
    # For web mode, expect URL as first argument after script name
    if len(filtered_argv) < 2:
        print("Error: URL required when using -w/--web option")
        sys.exit(1)
    img_source = filtered_argv[1]
    try:
        width = int(filtered_argv[2]) if len(filtered_argv) > 2 else 70
    except (IndexError, ValueError):
        width = 70
else:
    # For file mode, expect filename as first argument
    if len(filtered_argv) < 2:
        print("Error: Image file required")
        sys.exit(1)
    img_source = filtered_argv[1]
    try:
        width = int(filtered_argv[2]) if len(filtered_argv) > 2 else 70
    except (IndexError, ValueError):
        width = 70

# Read in the image with optional color support
if use_web:
    img = download_image_from_url(img_source)
else:
    try:
        img = Image.open(img_source)
    except FileNotFoundError:
        print(f"Error: File '{img_source}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error opening image file: {e}")
        sys.exit(1)
if use_color:
    # Keep original RGB for color information
    img_color = img.convert('RGB')
    img_gray = img.convert('L')
else:
    img_gray = img.convert('L')

# Enhance contrast and brightness for better ASCII conversion
enhancer = ImageEnhance.Contrast(img_gray)
img_gray = enhancer.enhance(contrast_factor)

# Resize the image as required with better resampling
orig_width, orig_height = img_gray.size
r = orig_height / orig_width
# The ASCII character glyphs are taller than they are wide. Maintain the aspect
# ratio by reducing the image height. Optimized for Slack's font rendering.
height = int(width * r * 0.5)  # Adjusted for Slack's monospace font characteristics
img_gray = img_gray.resize((width, height), Image.Resampling.LANCZOS)

if use_color:
    img_color = img_color.resize((width, height), Image.Resampling.LANCZOS)

# Now map the pixel brightness to the ASCII density glyphs with enhanced mapping
arr_gray = np.array(img_gray)
if use_color:
    arr_color = np.array(img_color)

# Apply brightness offset
arr_gray = np.clip(arr_gray + brightness_offset, 0, 255)

# Generate ASCII art lines
ascii_lines = []
for i in range(height):
    line = ""
    for j in range(width):
        p = arr_gray[i, j]
        # Optimized mapping for Slack's limited character set
        # Use simpler mapping that works better with fewer characters
        normalized = p / 255.0
        # Apply stronger gamma correction for better contrast with limited characters
        gamma_corrected = np.power(normalized, 0.6)  # Stronger correction
        # Map to density index with better precision
        k = int(gamma_corrected * (n - 1))
        k = min(k, n - 1)  # Ensure we don't exceed bounds
        
        char = density[n - 1 - k]
        
        if use_color:
            # Get RGB color for this pixel
            r, g, b = arr_color[i, j]
            line += get_ansi_color(r, g, b) + char + reset_color()
        else:
            line += char
    ascii_lines.append(line)

# Apply trimming if requested
if use_trim:
    ascii_lines = trim_ascii_art(ascii_lines)

# Output the final result
for line in ascii_lines:
    print(line)