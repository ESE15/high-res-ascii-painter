"""
Utility functions for ASCII art generator
"""

import os
import tempfile
import subprocess
from datetime import datetime
from .config import DENSITY_STRING


def get_ansi_color(r, g, b):
    """Convert RGB to ANSI 256-color code"""
    return f'\033[38;2;{r};{g};{b}m'


def reset_color():
    """Reset to default color"""
    return '\033[0m'


def save_clipboard_image():
    """
    Save clipboard image to a temporary file using PowerShell (WSL compatible)
    Returns the path to the saved image file
    """
    # Create temporary file
    temp_dir = tempfile.gettempdir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_filename = f"clipboard_image_{timestamp}.png"
    temp_path = os.path.join(temp_dir, temp_filename)
    
    # Convert to Windows path for PowerShell
    try:
        # Try wslpath if available (WSL environment)
        result = subprocess.run(['wslpath', '-w', temp_path], 
                              capture_output=True, text=True, check=True)
        win_path = result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: assume we're not in WSL or wslpath not available
        win_path = temp_path.replace('/', '\\')
    
    # PowerShell command to save clipboard image
    powershell_cmd = [
        'powershell.exe', '-NoProfile', '-Command',
        f"$img = Get-Clipboard -Format Image; "
        f"if (-not $img) {{ Write-Error 'No image found in clipboard'; exit 1 }}; "
        f"$img.Save('{win_path}',[System.Drawing.Imaging.ImageFormat]::Png)"
    ]
    
    try:
        # Execute PowerShell command
        result = subprocess.run(powershell_cmd, capture_output=True, text=True, check=True)
        
        # Check if file was created
        if os.path.exists(temp_path):
            print(f"Clipboard image saved to: {temp_path}")
            return temp_path
        else:
            raise FileNotFoundError("Failed to save clipboard image")
            
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown PowerShell error"
        raise RuntimeError(f"Failed to get image from clipboard: {error_msg}")
    except FileNotFoundError:
        raise RuntimeError("PowerShell not found. This feature requires Windows/WSL environment.")


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
    if DENSITY_STRING:
        background_chars.add(DENSITY_STRING[-1])  # Last character (space)
        if len(DENSITY_STRING) > 1:
            background_chars.add(DENSITY_STRING[-2])  # Second to last character ('.')
    else:
        background_chars = {' ', '.'}
    
    # Debug: print background characters
    print(f"Debug: Background characters detected: {background_chars}")
    print(f"Debug: Density string: '{DENSITY_STRING}'")
    
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
