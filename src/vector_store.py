import chromadb
from chromadb.utils import embedding_functions
from src.__init__ import get_api_key, get_gemini_model_config # get_gemini_model_configを追加

def get_embedding_function():
    """Gemini Embedding Functionを返す"""
    api_key = get_api_key("GEMINI_API_KEY")
    gemini_model_config = get_gemini_model_config() # 追加
    return embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=api_key,
        model_name=gemini_model_config['embedding'] # 変更
    )

def create_vector_store(texts: list[str], collection_name: str):
    """テキストチャンクからベクトルストアを作成し、永続化する"""
    client = chromadb.PersistentClient(path="./chroma_db") # 永続化パス
    embedding_function = get_embedding_function()

    # 既存のコレクションがあれば削除し、新規作成
    try:
        client.delete_collection(name=collection_name)
    except:
        pass # コレクションが存在しない場合はエラーにならない

    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    # ドキュメントとIDを追加
    # ChromaDBのaddメソッドはidsをリストで受け取る
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(
        documents=texts,
        ids=ids
    )
    return collection

def get_vector_store(collection_name: str):
    """既存のベクトルストアを取得する"""
    client = chromadb.PersistentClient(path="./chroma_db")
    embedding_function = get_embedding_function()
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    return collection

def retrieve_relevant_chunks(query: str, collection, n_results: int = 5) -> list[str]:
    """クエリに基づいて関連するチャンクを検索する"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results['documents'][0]
