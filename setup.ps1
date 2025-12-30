# Windows用セットアップスクリプト (PowerShell)

Write-Host "🌱 Blooming Garden 自動プレイヤー セットアップ 🌸" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# uvがインストールされているか確認
$uvExists = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvExists) {
    Write-Host "❌ uvがインストールされていません。" -ForegroundColor Red
    $response = Read-Host "📦 uvをインストールしますか？ (y/n)"
    
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "📥 uvをインストール中..." -ForegroundColor Yellow
        try {
            Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
            Write-Host "✅ uvのインストール完了" -ForegroundColor Green
            Write-Host "⚠️  PowerShellを再起動してから、再度このスクリプトを実行してください" -ForegroundColor Yellow
            Write-Host ""
            Read-Host "Enterキーを押して終了してください"
            exit 0
        }
        catch {
            Write-Host "❌ uvのインストールに失敗しました: $_" -ForegroundColor Red
            Write-Host "手動でインストールしてください: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
            Read-Host "Enterキーを押して終了してください"
            exit 1
        }
    }
    else {
        Write-Host "⚠️  uvなしで続行します（pipを使用）" -ForegroundColor Yellow
        $usePip = $true
    }
}
else {
    Write-Host "✅ uvが見つかりました" -ForegroundColor Green
    $usePip = $false
}

Write-Host ""
Write-Host "📦 依存関係をインストール中..." -ForegroundColor Cyan

try {
    if ($usePip) {
        # pipを使用
        Write-Host "仮想環境を作成中..." -ForegroundColor Yellow
        python -m venv .venv
        
        Write-Host "仮想環境を有効化中..." -ForegroundColor Yellow
        & .\.venv\Scripts\Activate.ps1
        
        Write-Host "Playwrightをインストール中..." -ForegroundColor Yellow
        pip install playwright
    }
    else {
        # uvを使用
        Write-Host "uvで依存関係を同期中..." -ForegroundColor Yellow
        uv sync
    }
    
    Write-Host "✅ 依存関係のインストール完了" -ForegroundColor Green
}
catch {
    Write-Host "❌ 依存関係のインストールに失敗しました: $_" -ForegroundColor Red
    Read-Host "Enterキーを押して終了してください"
    exit 1
}

Write-Host ""
Write-Host "🌐 Playwrightのブラウザをインストール中..." -ForegroundColor Cyan

try {
    if ($usePip) {
        playwright install chromium
    }
    else {
        uv run playwright install chromium
    }
    
    Write-Host "✅ ブラウザのインストール完了" -ForegroundColor Green
}
catch {
    Write-Host "❌ ブラウザのインストールに失敗しました: $_" -ForegroundColor Red
    Read-Host "Enterキーを押して終了してください"
    exit 1
}

Write-Host ""
Write-Host "🎉 セットアップ完了！" -ForegroundColor Green
Write-Host ""
Write-Host "📝 次のコマンドでゲームを自動プレイできます：" -ForegroundColor Cyan
Write-Host ""

if ($usePip) {
    Write-Host "  基本版:   python src\autoplay.py" -ForegroundColor White
    Write-Host "  高度版:   python src\autoplay_advanced.py" -ForegroundColor White
}
else {
    Write-Host "  基本版:   uv run python src/autoplay.py" -ForegroundColor White
    Write-Host "  高度版:   uv run python src/autoplay_advanced.py" -ForegroundColor White
}

Write-Host ""
Write-Host "💡 ヒント: run_autoplay.ps1 を実行すると簡単に起動できます" -ForegroundColor Yellow
Write-Host ""

Read-Host "Enterキーを押して終了してください"
