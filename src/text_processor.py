from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from src.__init__ import get_api_key, get_gemini_model_config # get_gemini_model_configを追加

def split_text_into_chunks(text: str) -> list[str]:
    """テキストをチャンクに分割する"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def summarize_text(text: str) -> str:
    """テキストを要約する"""
    genai.configure(api_key=get_api_key("GEMINI_API_KEY"))
    gemini_model_config = get_gemini_model_config() # 追加
    model = genai.GenerativeModel(gemini_model_config['summary']) # 変更

    prompt = f"以下のドキュメントを要約してください:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
