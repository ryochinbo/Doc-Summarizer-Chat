import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import io

def load_text_from_url(url: str) -> str:
    """URLからテキストを抽出する"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        soup = BeautifulSoup(response.text, 'html.parser')
        # スクリプトやスタイルタグを除去
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        # 連続する空白文字を1つにまとめる
        return " ".join(text.split())
    except requests.exceptions.RequestException as e:
        return f"URLの読み込み中にエラーが発生しました: {e}"

def load_text_from_pdf(uploaded_file) -> str:
    """アップロードされたPDFファイルからテキストを抽出する"""
    text = ""
    try:
        # BytesIOオブジェクトからPDFドキュメントを開く
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"PDFの読み込み中にエラーが発生しました: {e}"

def load_text_from_txt(uploaded_file) -> str:
    """アップロードされたテキストファイルからテキストを抽出する"""
    try:
        return uploaded_file.read().decode("utf-8")
    except Exception as e:
        return f"テキストファイルの読み込み中にエラーが発生しました: {e}"

def load_text_from_markdown(uploaded_file) -> str:
    """アップロードされたMarkdownファイルからテキストを抽出する"""
    try:
        return uploaded_file.read().decode("utf-8")
    except Exception as e:
        return f"Markdownファイルの読み込み中にエラーが発生しました: {e}"

def load_text_from_input(input_text: str) -> str:
    """直接入力されたテキストを返す"""
    return input_text
