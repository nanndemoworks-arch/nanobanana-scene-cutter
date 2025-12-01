# 🚀 Streamlit Cloud デプロイ手順

## 📋 必要なもの
- GitHubアカウント
- 作成したファイル一式（app.py、requirements.txt、README.md）

## ステップ1: GitHubにアップロード

### 1-1. GitHubで新規リポジトリを作成
1. https://github.com にアクセス
2. 右上の「+」→「New repository」
3. リポジトリ名を入力（例: `nanobanana-scene-cutter`）
4. Public を選択
5. 「Create repository」をクリック

### 1-2. ファイルをアップロード
以下の方法のどちらかを使います：

#### 方法A: ブラウザから直接アップロード（簡単）
1. 作成したリポジトリページで「uploading an existing file」をクリック
2. 以下のファイルをドラッグ&ドロップ:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
3. 「Commit changes」をクリック

#### 方法B: Git コマンド（慣れている人向け）
```bash
cd /path/to/your/files
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nanobanana-scene-cutter.git
git push -u origin main
```

## ステップ2: Streamlit Cloud でデプロイ

### 2-1. Streamlit Cloud にサインイン
1. https://streamlit.io/cloud にアクセス
2. 「Sign in」→「Continue with GitHub」
3. GitHubアカウントでログイン

### 2-2. アプリをデプロイ
1. 「New app」をクリック
2. 以下を入力:
   - **Repository**: 作成したリポジトリを選択
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. 「Deploy!」をクリック

### 2-3. デプロイ完了を待つ
- 数分待つと自動的にアプリが起動します
- URLが発行されます（例: `https://your-app.streamlit.app`）

## ステップ3: 友達に共有

### URLを共有
- 発行されたURLを友達に送る
- 例: `https://nanobanana-scene-cutter.streamlit.app`

### 使い方を説明
友達に以下を伝えてください：

```
📱 使い方:

1. このURL にアクセス: [あなたのアプリURL]

2. fal.ai でAPIキーを取得:
   - https://fal.ai でアカウント作成（無料）
   - ダッシュボードで API Key をコピー

3. アプリにAPIキーを入力

4. 画像をアップロードして生成開始！

💰 料金: 
- 1K解像度: $0.15/回
- 4K解像度: $0.30/回
- 新規アカウントで無料クレジットあり
```

## 🔧 トラブルシューティング

### デプロイがエラーになる
- requirements.txt の内容を確認
- Streamlit Cloud のログを確認

### アプリが動かない
- ブラウザのキャッシュをクリア
- Streamlit Cloud で「Reboot app」を試す

### パッケージのバージョンエラー
requirements.txt のバージョンを調整:
```
streamlit
fal-client
Pillow
requests
```
（バージョン指定を削除）

## 📝 更新方法

### コードを更新したい時
1. GitHubのリポジトリでファイルを編集
2. 変更をコミット
3. Streamlit Cloud が自動的に再デプロイ

または:
- Streamlit Cloud のダッシュボードで「Reboot app」

## 🎉 完成！

あなたのアプリが世界中からアクセス可能になりました！
URLを友達に共有して使ってもらいましょう。

---

**ヒント**: 
- アプリは完全無料でホスティングできます
- ユーザーが自分のAPIキーを使うので、あなたに費用はかかりません
- 困ったら Streamlit Community Forum で質問できます
