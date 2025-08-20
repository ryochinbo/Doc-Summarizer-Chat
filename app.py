import streamlit as st
from src.data_loader import load_text_from_url, load_text_from_pdf, load_text_from_txt, load_text_from_markdown, load_text_from_input
from src.text_processor import split_text_into_chunks, summarize_text
from src.vector_store import create_vector_store, get_vector_store
from src.chatbot import get_rag_response
from src.ui import display_sidebar, display_info_collection_ui, display_chat_ui, display_markdown_content, display_summary_area
import uuid # コレクション名の一意性を保つため

def main():
    st.set_page_config(page_title="DocQuery-Streamlit", layout="wide")

    # セッションステートの初期化
    if "processed_text" not in st.session_state:
        st.session_state.processed_text = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "collection_name" not in st.session_state:
        st.session_state.collection_name = None
    if "db_built" not in st.session_state:
        st.session_state.db_built = False
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "情報収集モード" # 初期モード

    # サイドバーの表示とモード選択
    st.session_state.current_mode = display_sidebar()

    # メインエリア
    st.title("DocQuery-Streamlit")

    if st.session_state.current_mode == "情報収集モード":
        source_type, content = display_info_collection_ui()

        if st.button("読み込み・要約"):
            if content:
                with st.spinner("情報を読み込み中..."):
                    if source_type == "URL":
                        st.session_state.processed_text = load_text_from_url(content)
                    elif source_type == "PDFアップロード":
                        st.session_state.processed_text = load_text_from_pdf(content)
                    elif source_type == "テキスト入力":
                        st.session_state.processed_text = load_text_from_input(content)
                    elif source_type == "Markdownアップロード": # Markdownアップロードも追加
                        st.session_state.processed_text = load_text_from_markdown(content)

                    if st.session_state.processed_text:
                        st.success("情報の読み込みが完了しました！")
                        # DB構築
                        with st.spinner("データベースを構築中..."):
                            chunks = split_text_into_chunks(st.session_state.processed_text)
                            st.session_state.collection_name = f"doc_collection_{uuid.uuid4().hex}"
                            create_vector_store(chunks, st.session_state.collection_name)
                            st.session_state.db_built = True
                            st.success("データベースの構築が完了しました！")

                        # 要約
                        with st.spinner("要約を生成中..."):
                            st.session_state.summary = summarize_text(st.session_state.processed_text)
                            st.success("要約の生成が完了しました！")
                    else:
                        st.error("情報の読み込みに失敗しました。")
            else:
                st.warning("情報ソースを入力または選択してください。")

        # 読み込みコンテンツ表示
        if st.session_state.processed_text:
            display_markdown_content("読み込みコンテンツ", st.session_state.processed_text)

        # 要約結果表示
        if st.session_state.summary:
            display_summary_area(st.session_state.summary)

    elif st.session_state.current_mode == "質問チャットモード":
        if not st.session_state.db_built:
            st.warning("RAGチャットを利用するには、まず情報収集モードで情報を読み込み、データベースを構築してください。")
            return

        display_chat_ui(st.session_state.chat_history)

        if prompt := st.chat_input("質問を入力してください..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.spinner("回答を生成中..."):
                response = get_rag_response(prompt, st.session_state.collection_name)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.experimental_rerun() # チャット履歴を更新するために再実行

if __name__ == "__main__":
    main()
