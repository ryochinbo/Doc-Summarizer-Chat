# DocQuery-Streamlit

## 概要

DocQuery-Streamlitは、Webページ、PDFファイル、テキスト、Markdownファイルから情報を取得し、その内容を要約したり、RAG (Retrieval-Augmented Generation) を用いて質問応答を行うことができるStreamlitアプリケーションです。

## 機能

*   **情報取得**:
    *   WebページのURLから本文テキストを抽出。
    *   PDFファイル、テキストファイル、Markdownファイルからテキストを抽出。
    *   直接入力されたテキストを利用。
*   **要約**: 取得した情報ソースの全文を大規模言語モデル (LLM) で要約。
*   **DB構築**: 取得したテキストをチャンクに分割し、Embeddingモデルでベクトル化後、メモリ上のベクトルデータベース (ChromaDB) に保存。
*   **質問応答 (RAGチャット)**: ユーザーの質問とベクトルデータベースから検索された関連チャンクを基に、LLMが回答を生成。

## 技術スタック

*   **Webフレームワーク**: Streamlit
*   **言語**: Python
*   **LLM連携・RAGフレームワーク**: LangChain
*   **LLM**: Google AI (Gemini)
*   **ベクトルデータベース**: ChromaDB (インメモリ)
*   **Webスクレイピング**: BeautifulSoup4
*   **PDF読み込み**: PyMuPDF

## セットアップ

### 1. APIキーの設定

Gemini APIを利用するため、APIキーが必要です。
プロジェクトのルートディレクトリに`.streamlit/secrets.yaml`ファイルを作成し、以下の形式でAPIキーを記述してください。

```yaml
GEMINI_API_KEY: "YOUR_GEMINI_API_KEY"
```

`YOUR_GEMINI_API_KEY`の部分を、ご自身のGemini APIキーに置き換えてください。

### 2. 依存関係のインストール

プロジェクトに必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

## 実行方法

セットアップが完了したら、以下のコマンドでアプリケーションを起動できます。

```bash
streamlit run app.py
```

アプリケーションがブラウザで開きます。

## ディレクトリ構成

```
DocQuery-Streamlit/
│
├── .streamlit/
│   └── secrets.yaml          # APIキーや設定情報を安全に管理
│   └── secrets.sample.yaml   # APIキーや設定情報の変数設定形式をレポジトリをクローンされる方向けに共有
├── src/
│   ├── __init__.py           # このディレクトリをPythonパッケージとして認識させる
│   ├── data_loader.py        # URL、PDF、テキストからのデータ読み込み処理
│   ├── text_processor.py     # テキストの分割や要約処理
│   ├── vector_store.py       # ベクトルデータベースの作成と検索処理
│   ├── chatbot.py            # 質問応答（RAG）チェーンの構築と実行
│   └── ui.py                 # StreamlitのUIコンポーネントを定義するヘルパー関数
│
├── app.py                    # Streamlitアプリケーションのエントリーポイント
├── requirements.txt          # プロジェクトの依存ライブラリ一覧
├── .gitignore                # Gitの追跡から除外するファイルを指定
└── README.md                 # プロジェクトの概要、セットアップ方法、使い方を記載
```