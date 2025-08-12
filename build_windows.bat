@echo off
echo Building ASCII Painter for Windows...
python build_windows.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Build completed successfully!
    echo 📁 Check dist/windows/ folder for the executable
    echo.
    pause
) else (
    echo.
    echo ❌ Build failed!
    echo.
    pause
)
