@echo off
setlocal enabledelayedexpansion

title Blooming Garden Setup

echo Blooming Garden Auto Player Setup
echo ================================================
echo.

REM Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] uv is not installed.
    echo.
    set /p response="Install uv? (y/n): "
    if /i "!response!"=="y" (
        echo Installing uv...
        powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo [SUCCESS] uv installation completed
            echo.
            echo [WARNING] Please restart Command Prompt and run this script again
        ) else (
            echo.
            echo [ERROR] uv installation failed
            echo Please install manually: https://docs.astral.sh/uv/getting-started/installation/
        )
        echo.
        pause
        exit /b 0
    ) else (
        echo [INFO] Continue without uv (using pip)
        set USE_PIP=true
    )
) else (
    echo [SUCCESS] uv found
    set USE_PIP=false
)

echo.
echo Installing dependencies...
echo.

if "!USE_PIP!"=="true" (
    REM Use pip
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    
    echo Installing Playwright...
    pip install playwright
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install Playwright
        pause
        exit /b 1
    )
) else (
    REM Use uv
    echo Syncing dependencies with uv...
    uv sync
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to sync dependencies
        pause
        exit /b 1
    )
)

echo.
echo [SUCCESS] Dependencies installed
echo.

echo Installing Playwright browser...
echo.

if "!USE_PIP!"=="true" (
    playwright install chromium
) else (
    uv run playwright install chromium
)

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install browser
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Browser installed
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo You can now run the auto player with:
echo.
if "!USE_PIP!"=="true" (
    echo   Basic:    python src\autoplay.py
    echo   Advanced: python src\autoplay_advanced.py
) else (
    echo   Basic:    uv run python src/autoplay.py
    echo   Advanced: uv run python src/autoplay_advanced.py
)
echo.
echo TIP: Double-click run_autoplay.bat for easy launch
echo.
echo ============================================
echo.

pause
