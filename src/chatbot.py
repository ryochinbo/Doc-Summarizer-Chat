import google.generativeai as genai
from src.vector_store import retrieve_relevant_chunks, get_vector_store
from src.__init__ import get_api_key, get_gemini_model_config # get_gemini_model_configを追加

def get_rag_response(question: str, collection_name: str) -> str:
    """RAGに基づいて質問に回答する"""
    genai.configure(api_key=get_api_key("GEMINI_API_KEY"))
    gemini_model_config = get_gemini_model_config() # 追加
    model = genai.GenerativeModel(gemini_model_config['chat']) # 変更

    # ベクトルストアから関連チャンクを取得
    vector_store_collection = get_vector_store(collection_name)
    relevant_chunks = retrieve_relevant_chunks(question, vector_store_collection)

    # プロンプトの構築
    context = "\n".join(relevant_chunks)
    prompt = f"""以下のコンテキストに基づいて質問に答えてください。
もしコンテキストに関連する情報がない場合は、「提供された情報からは回答できません。」と答えてください。

コンテキスト:
{context}

質問:
{question}
"""
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    return response.text
