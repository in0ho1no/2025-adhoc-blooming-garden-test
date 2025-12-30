# 🚀 クイックスタート

Blooming Gardenを自動プレイするための最速セットアップガイド

## ⚡ 3ステップで開始

### 1️⃣ セットアップ
`setup.ps1` を右クリック → **「PowerShellで実行」**

### 2️⃣ 実行
`run_autoplay.ps1` を右クリック → **「PowerShellで実行」**

### 3️⃣ 楽しむ
ブラウザが自動で開いてゲームが始まります！🎮

---

## ⚠️ PowerShell実行ポリシーについて

初回実行時に「スクリプトの実行が無効」エラーが出る場合：

1. PowerShellを**管理者として**開く
2. 以下を実行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
3. `Y` を入力してEnter

これは一度だけ実行すればOKです。

---

## 💡 よくある質問

### Q: uvって何？
A: Pythonの超高速パッケージマネージャーです。setup.ps1が自動でインストールしてくれます。

### Q: エラーが出た
A: 以下を確認してください：
- Python 3.12以上がインストールされているか
- setup.ps1を実行したか
- PowerShellを再起動したか
- 実行ポリシーを設定したか（上記参照）

### Q: 手動で実行したい
A: PowerShellで以下を実行：
```powershell
uv run python src/autoplay.py
```

### Q: もっと詳しく知りたい
A: `README.md` を参照してください

---

## 🎯 2つのモード

| モード | 特徴 |
|--------|------|
| **基本版** | シンプル・高速 |
| **高度版** | 賢い戦略・高スコア |

`run_autoplay.ps1` 実行時に選択できます！

---

**それでは、良い自動プレイを！** 🌱🌸
