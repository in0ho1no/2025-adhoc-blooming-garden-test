@echo off
setlocal enabledelayedexpansion

title Blooming Garden Auto Player

echo Blooming Garden Auto Player
echo ================================
echo.

timeout /t 1 /nobreak >nul

echo Which mode do you want to run?
echo.
echo 1. Basic (Simple strategy)
echo 2. Advanced (Grid analysis strategy)
echo.

set /p choice="Enter number (1 or 2): "

echo.

REM Check if uv is available
where uv >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set USE_UV=true
) else (
    set USE_UV=false
)

if "!choice!"=="1" (
    echo Launching Basic mode...
    echo.
    if "!USE_UV!"=="true" (
        uv run python src/autoplay.py
    ) else (
        python src\autoplay.py
    )
) else if "!choice!"=="2" (
    echo Launching Advanced mode...
    echo.
    if "!USE_UV!"=="true" (
        uv run python src/autoplay_advanced.py
    ) else (
        python src\autoplay_advanced.py
    )
) else (
    echo.
    echo [ERROR] Invalid choice. Please enter 1 or 2.
)

echo.
echo ============================================
echo.

pause
