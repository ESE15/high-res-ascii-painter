#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 포터블 실행 파일 빌드 스크립트
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Windows에서 UTF-8 출력 설정
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def build_windows_executable():
    """PyInstaller를 사용하여 Windows 실행 파일을 빌드"""
    
    print("Building Windows portable executable...")
    
    # 플랫폼 확인 및 경고
    import platform
    current_os = platform.system()
    if current_os != "Windows":
        print(f"WARNING: Building on {current_os} for Windows target")
        print("Cross-compilation may not work properly!")
        print("For best results, run this build on Windows")
        print()
    
    # 빌드 디렉토리 정리
    build_dirs = ['build', 'dist']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned up {dir_name} directory")
    
    # PyInstaller 명령어 구성
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',  # 단일 실행 파일로 생성
        '--console',  # 콘솔 애플리케이션
        '--name', 'ascii-painter',  # 실행 파일 이름
        '--distpath', 'dist/windows',  # 출력 디렉토리
        '--workpath', 'build/windows',  # 임시 빌드 디렉토리
        '--specpath', 'build',  # spec 파일 위치
        '--clean',  # 빌드 전 정리
        '--noconfirm',  # 확인 없이 덮어쓰기
        # 숨겨진 import 추가 (필요한 경우)
        '--hidden-import', 'PIL._tkinter_finder',
        '--hidden-import', 'numpy',
        '--hidden-import', 'requests',
        # 메인 스크립트
        'src/high_res_ascii_painter/painter.py'
    ]
    
    try:
        # PyInstaller 실행
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        print("PyInstaller build successful!")
        
        # 빌드 결과 확인 (Linux에서 빌드시 .exe 확장자가 없을 수 있음)
        exe_path = Path('dist/windows/ascii-painter.exe')
        exe_path_no_ext = Path('dist/windows/ascii-painter')
        
        actual_exe_path = None
        if exe_path.exists():
            actual_exe_path = exe_path
        elif exe_path_no_ext.exists():
            actual_exe_path = exe_path_no_ext
            # 확장자 추가
            exe_path_no_ext.rename(exe_path)
            actual_exe_path = exe_path
        
        if actual_exe_path and actual_exe_path.exists():
            file_size = actual_exe_path.stat().st_size / (1024 * 1024)  # MB 단위
            print(f"Executable created: {actual_exe_path}")
            print(f"File size: {file_size:.1f} MB")
            
            # README 파일 생성
            create_windows_readme()
            
            return True
        else:
            print("ERROR: Executable not found after build")
            print("Available files in dist/windows:")
            dist_path = Path('dist/windows')
            if dist_path.exists():
                for file in dist_path.iterdir():
                    print(f"  - {file.name}")
            return False
            
    except subprocess.CalledProcessError as e:
        print("ERROR: PyInstaller build failed:")
        print(f"Error: {e.stderr}")
        return False

def create_windows_readme():
    """Windows용 README 파일 생성"""
    readme_content = """# ASCII Painter - Windows Portable

Slack-Optimized ASCII Art Generator for Windows

## Usage

Open Command Prompt or PowerShell and run:

```cmd
# Basic usage
ascii-painter.exe image.jpg 70

# From web URL
ascii-painter.exe -w https://picsum.photos/400/300 60

# From clipboard (automatic!)
ascii-painter.exe --clip 80 --trim

# Auto-copy result to clipboard
ascii-painter.exe image.jpg 70 -a --trim

# Full automation: clipboard → ASCII → clipboard
ascii-painter.exe --clip 80 --trim -a
```

## Options

- `-w, --web`: Download image from URL instead of local file
- `--clip, -v`: Use image from clipboard (requires PowerShell)
- `-a, --auto-copy`: Copy ASCII art result to clipboard automatically  
- `--color, -c`: Enable colored output (not recommended for Slack)
- `--trim, -t`: Remove background-only rows and columns for compact output
- `--help, -h`: Show help message

## Clipboard Features

### Input (--clip)
- Uses PowerShell to get image from clipboard
- Copy any image or take screenshot before running
- Temporary files are automatically cleaned up

### Output (-a, --auto-copy)  
- Uses PowerShell to copy ASCII art to clipboard
- Perfect for pasting directly into Slack with code blocks (```)
- Works with any output mode

## Slack Tips

- Use width 60-80 for best results in Slack code blocks
- Copy output and paste into Slack using code block (```)
- Avoid color mode when pasting to Slack

## Examples

```cmd
# Convert local image and copy to clipboard
ascii-painter.exe photo.jpg 70 -a --trim

# Screenshot workflow: 
# 1. Take screenshot (Win+Shift+S)
# 2. Run: ascii-painter.exe --clip 80 --trim -a  
# 3. Paste in Slack with ```

# Web image workflow:
ascii-painter.exe -w https://picsum.photos/400/300 60 -a
```

## Requirements

- Windows 10/11
- PowerShell (for clipboard features)
- No Python installation required!

## File Info

This is a portable executable - no installation needed.
Just download and run from anywhere on your Windows system.
"""
    
    readme_path = Path('dist/windows/README.md')
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Windows README created: {readme_path}")

def create_build_script():
    """빌드용 배치 파일 생성"""
    batch_content = """@echo off
echo Building ASCII Painter for Windows...
python build_windows.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build completed successfully!
    echo Check dist/windows/ folder for the executable
    echo.
    pause
) else (
    echo.
    echo Build failed!
    echo.
    pause
)
"""
    
    with open('build_windows.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print("Windows build script created: build_windows.bat")

if __name__ == "__main__":
    print("ASCII Painter Windows Build Tool")
    print("=" * 50)
    
    # 빌드 실행
    success = build_windows_executable()
    
    # 배치 파일 생성
    create_build_script()
    
    if success:
        print("\nBuild completed successfully!")
        print("Check dist/windows/ folder for:")
        print("   - ascii-painter.exe (main executable)")
        print("   - README.md (usage instructions)")
        print("\nYou can also use build_windows.bat for future builds")
    else:
        print("\nBuild failed. Check error messages above.")
    
    print("\n" + "=" * 50)
