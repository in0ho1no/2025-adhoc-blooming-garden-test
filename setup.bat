@echo off
REM Windows用セットアップスクリプト

echo 🌱 Blooming Garden 自動プレイヤー セットアップ 🌸
echo ================================================
echo.

REM uvがインストールされているか確認
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ uvがインストールされていません。
    echo 📦 uvをインストールしますか？ ^(y/n^)
    set /p response=
    if /i "%response%"=="y" (
        echo 📥 uvをインストール中...
        powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
        echo ✅ uvのインストール完了
        echo ⚠️  PowerShellまたはコマンドプロンプトを再起動してください
        pause
        exit /b 0
    ) else (
        echo ⚠️  uvなしで続行します^(pipを使用^)
        set USE_PIP=true
    )
) else (
    echo ✅ uvが見つかりました
    set USE_PIP=false
)

echo.
echo 📦 依存関係をインストール中...

if "%USE_PIP%"=="true" (
    REM pipを使用
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install playwright
) else (
    REM uvを使用
    uv sync
)

echo ✅ 依存関係のインストール完了
echo.

echo 🌐 Playwrightのブラウザをインストール中...

if "%USE_PIP%"=="true" (
    playwright install chromium
) else (
    uv run playwright install chromium
)

echo ✅ ブラウザのインストール完了
echo.

echo 🎉 セットアップ完了！
echo.
echo 📝 次のコマンドでゲームを自動プレイできます：
echo.
if "%USE_PIP%"=="true" (
    echo   基本版:   python src\autoplay.py
    echo   高度版:   python src\autoplay_advanced.py
) else (
    echo   基本版:   uv run python src/autoplay.py
    echo   高度版:   uv run python src/autoplay_advanced.py
)
echo.

pause
