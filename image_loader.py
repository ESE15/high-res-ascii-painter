"""
Image loading functionality for ASCII art generator
"""

import sys
import requests
from PIL import Image
from io import BytesIO
from config import WEB_HEADERS, DEFAULT_TIMEOUT


def download_image_from_url(url):
    """Download image from URL and return PIL Image object"""
    try:
        print(f"Downloading image from: {url}")
        
        # Special handling for known problematic domains
        if 'slack.com' in url:
            print("Warning: Slack files require authentication and may not be accessible directly.")
            print("Consider downloading the image manually and using a local file instead.")
            print("Alternative: Use a public image hosting service like imgur, picsum.photos, etc.")
        
        response = requests.get(url, headers=WEB_HEADERS, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
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


def load_image_from_file(file_path):
    """Load image from local file and return PIL Image object"""
    try:
        img = Image.open(file_path)
        return img
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error opening image file: {e}")
        sys.exit(1)


def load_image(source, is_web=False):
    """Load image from either web URL or local file"""
    if is_web:
        return download_image_from_url(source)
    else:
        return load_image_from_file(source)
