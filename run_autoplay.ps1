# Blooming Garden 自動プレイ実行スクリプト (PowerShell)

Write-Host "🌱 Blooming Garden 自動プレイヤー 🌸" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "どちらのモードで実行しますか？" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 基本版（シンプルな戦略）" -ForegroundColor White
Write-Host "2. 高度版（グリッド分析戦略）" -ForegroundColor White
Write-Host ""

$choice = Read-Host "番号を入力してください (1 または 2)"

Write-Host ""

# uvが使用可能かチェック
$uvExists = Get-Command uv -ErrorAction SilentlyContinue

switch ($choice) {
    "1" {
        Write-Host "🚀 基本版を起動中..." -ForegroundColor Yellow
        if ($uvExists) {
            uv run python src/autoplay.py
        }
        else {
            python src\autoplay.py
        }
    }
    "2" {
        Write-Host "🚀 高度版を起動中..." -ForegroundColor Yellow
        if ($uvExists) {
            uv run python src/autoplay_advanced.py
        }
        else {
            python src\autoplay_advanced.py
        }
    }
    default {
        Write-Host "❌ 無効な選択です。1 または 2 を入力してください。" -ForegroundColor Red
    }
}

Write-Host ""
Read-Host "Enterキーを押して終了してください"
