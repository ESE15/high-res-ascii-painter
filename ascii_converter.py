"""
ASCII art conversion functionality
"""

import numpy as np
from PIL import Image, ImageEnhance
from config import (
    DENSITY_STRING, 
    CONTRAST_FACTOR, 
    BRIGHTNESS_OFFSET, 
    ASPECT_RATIO_CORRECTION, 
    GAMMA_CORRECTION
)
from utils import get_ansi_color, reset_color


class ASCIIConverter:
    """Handles conversion of images to ASCII art"""
    
    def __init__(self, use_color=False):
        self.use_color = use_color
        self.density = DENSITY_STRING
        self.n = len(self.density)
    
    def prepare_image(self, img, width):
        """Prepare image for ASCII conversion by resizing and enhancing"""
        # Convert to appropriate color mode
        if self.use_color:
            img_color = img.convert('RGB')
            img_gray = img.convert('L')
        else:
            img_gray = img.convert('L')
        
        # Enhance contrast and brightness for better ASCII conversion
        enhancer = ImageEnhance.Contrast(img_gray)
        img_gray = enhancer.enhance(CONTRAST_FACTOR)
        
        # Resize the image as required with better resampling
        orig_width, orig_height = img_gray.size
        r = orig_height / orig_width
        # The ASCII character glyphs are taller than they are wide. Maintain the aspect
        # ratio by reducing the image height. Optimized for Slack's font rendering.
        height = int(width * r * ASPECT_RATIO_CORRECTION)
        img_gray = img_gray.resize((width, height), Image.Resampling.LANCZOS)
        
        if self.use_color:
            img_color = img_color.resize((width, height), Image.Resampling.LANCZOS)
            return img_gray, img_color, width, height
        else:
            return img_gray, None, width, height
    
    def convert_to_ascii(self, img, width):
        """Convert image to ASCII art"""
        img_gray, img_color, final_width, height = self.prepare_image(img, width)
        
        # Convert to numpy arrays
        arr_gray = np.array(img_gray)
        if self.use_color:
            arr_color = np.array(img_color)
        
        # Apply brightness offset
        arr_gray = np.clip(arr_gray + BRIGHTNESS_OFFSET, 0, 255)
        
        # Generate ASCII art lines
        ascii_lines = []
        for i in range(height):
            line = ""
            for j in range(final_width):
                p = arr_gray[i, j]
                # Optimized mapping for Slack's limited character set
                # Use simpler mapping that works better with fewer characters
                normalized = p / 255.0
                # Apply stronger gamma correction for better contrast with limited characters
                gamma_corrected = np.power(normalized, GAMMA_CORRECTION)
                # Map to density index with better precision
                k = int(gamma_corrected * (self.n - 1))
                k = min(k, self.n - 1)  # Ensure we don't exceed bounds
                
                char = self.density[self.n - 1 - k]
                
                if self.use_color:
                    # Get RGB color for this pixel
                    r, g, b = arr_color[i, j]
                    line += get_ansi_color(r, g, b) + char + reset_color()
                else:
                    line += char
            ascii_lines.append(line)
        
        return ascii_lines
