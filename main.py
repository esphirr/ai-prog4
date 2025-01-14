import streamlit as st

# Page Configuration
st.set_page_config(page_title="MemoMemo", layout="wide")

# Link external CSS file
def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# State initialization
if "memos" not in st.session_state:
    st.session_state.memos = []
if "current_memo_index" not in st.session_state:
    st.session_state.current_memo_index = None

# Functions
def reset_panel():
    st.session_state.memo_title = ""
    st.session_state.memo_content = ""
    st.session_state.selected_tags = []
    st.session_state.current_memo_index = None

def save_memo():
    if st.session_state.memo_title and st.session_state.memo_content:
        memo = {
            "title": st.session_state.memo_title,
            "content": st.session_state.memo_content,
            "tags": st.session_state.selected_tags,
            "date": st.session_state.memo_date
        }
        if st.session_state.current_memo_index is not None:
            st.session_state.memos[st.session_state.current_memo_index] = memo
        else:
            st.session_state.memos.append(memo)
        reset_panel()
    else:
        st.error("タイトルと内容を入力してください。")

def delete_memo():
    if st.session_state.current_memo_index is not None:
        del st.session_state.memos[st.session_state.current_memo_index]
        reset_panel()

def edit_memo(index):
    memo = st.session_state.memos[index]
    st.session_state.memo_title = memo["title"]
    st.session_state.memo_content = memo["content"]
    st.session_state.selected_tags = memo["tags"]
    st.session_state.current_memo_index = index

def filter_memos_by_tag(tag):
    if tag == "all":
        return st.session_state.memos
    return [memo for memo in st.session_state.memos if tag in memo["tags"]]

def search_memos(query):
    return [memo for memo in st.session_state.memos if query.lower() in memo["title"].lower()]

# Sidebar
with st.sidebar:
    st.header("タグ")
    tags = ["to-do", "priority", "note", "work", "training", "daily"]
    selected_tag = st.radio("フィルタを選択", ["all"] + tags, key="filter_tag")
    filtered_memos = filter_memos_by_tag(selected_tag)

# Main container
st.title("MemoMemo")
st.subheader("ホーム")

# Search bar
search_query = st.text_input("タグ検索", key="search_query")
if search_query:
    filtered_memos = search_memos(search_query)

# Display memos
for index, memo in enumerate(filtered_memos):
    with st.container():
        st.write(f"### {memo['title']}")
        st.write(memo['content'])
        st.write(f"Tags: {', '.join(memo['tags'])}")
        if st.button("編集", key=f"edit_{index}"):
            edit_memo(index)
        st.write("---")

# New Memo Panel
st.subheader("新規メモ作成")
st.text_input("メモのタイトル", key="memo_title")
st.text_area("メモの内容", key="memo_content", height=200)
st.date_input("作成日", key="memo_date")

# Tags selection
st.multiselect("タグを選択", options=tags, key="selected_tags")

# Panel Footer
if st.button("✔ 保存"):
    save_memo()

if st.session_state.current_memo_index is not None and st.button("削除"):
    delete_memo()

if st.button("✖ キャンセル"):
    reset_panel()
