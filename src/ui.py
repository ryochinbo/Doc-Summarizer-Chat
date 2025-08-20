import streamlit as st

def display_sidebar():
    """サイドバーを表示する"""
    with st.sidebar:
        st.title("DocQuery-Streamlit")
        st.markdown("---")
        st.subheader("モード選択")
        mode = st.radio(
            "どちらのモードで利用しますか？",
            ("情報収集モード", "質問チャットモード"),
            key="mode_selection"
        )
        st.markdown("---")
        return mode

def display_info_collection_ui():
    """情報収集モードのUIを表示する"""
    st.subheader("情報ソースの選択")
    source_type = st.radio(
        "情報ソースを選択してください:",
        ("URL", "PDFアップロード", "テキスト入力", "Markdownアップロード"), # ここにMarkdownアップロードを追加
        key="source_type"
    )

    content = None
    if source_type == "URL":
        url = st.text_input("URLを入力してください:", key="url_input")
        if url:
            content = url
    elif source_type == "PDFアップロード":
        uploaded_file = st.file_uploader("PDFファイルをアップロードしてください:", type=["pdf"], key="pdf_uploader")
        if uploaded_file:
            content = uploaded_file
    elif source_type == "テキスト入力":
        input_text = st.text_area("テキストを直接入力してください:", height=300, key="text_input_area")
        if input_text:
            content = input_text
    elif source_type == "Markdownアップロード": # Markdownアップロードの処理を追加
        uploaded_file = st.file_uploader("Markdownファイルをアップロードしてください:", type=["md"], key="md_uploader")
        if uploaded_file:
            content = uploaded_file
    return source_type, content

def display_chat_ui(chat_history):
    """質問チャットモードのUIを表示する"""
    st.subheader("質問チャット")
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力はapp.pyで処理するため、ここでは表示のみ
    # st.chat_input("質問を入力してください...")

def display_markdown_content(title: str, content: str):
    """Markdown形式のコンテンツを表示する"""
    st.subheader(title)
    st.markdown(content)

def display_summary_area(summary: str):
    """要約結果表示エリアを表示する"""
    st.subheader("要約結果")
    if summary:
        st.write(summary)
    else:
        st.info("要約がまだ生成されていません。")