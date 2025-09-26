# Mikan Mode Development Setup

## VPS開発環境セットアップ完了

### 📁 プロジェクト場所
```
~/.pg/development-projects/mikan-mode-v4/
```

### 🐍 Python環境
```bash
cd ~/.pg/development-projects/mikan-mode-v4
source venv/bin/activate
```

### 📦 依存関係インストール
```bash
pip install -r requirements.txt
```

### 🔄 Git管理
- ✅ リポジトリ初期化済み
- ✅ 初回コミット完了
- ✅ .gitignore設定済み

### 🛠️ 開発ワークフロー

1. **仮想環境アクティベート**
   ```bash
   cd ~/.pg/development-projects/mikan-mode-v4
   source venv/bin/activate
   ```

2. **コード編集**
   - Claude Codeでファイル編集

3. **テスト・ビルド**
   ```bash
   # コード品質チェック
   black .
   mypy .

   # Ankiアドオンパッケージ作成
   zip -r mikan_mode_v4.ankiaddon manifest.json __init__.py *.py
   ```

4. **Git管理**
   ```bash
   git add .
   git commit -m "Description"
   ```

### 📋 次のステップ
- Ankiアドオン配布形式(.ankiaddon)の作成
- テスト環境でのデバッグ
- 機能拡張・改善
- GitHubリポジトリ作成・公開