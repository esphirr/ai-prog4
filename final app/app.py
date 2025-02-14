# main class
# library import
import streamlit as st
import requests
import json
from datetime import datetime
# pyfile import
from config import API_URL
from memo_class import generate_memo, show_all_memos, search_by_tag, manage_tags


# メインエリア
st.set_page_config(page_title="📝MemoMemo📝", layout="wide")
st.title("📝MemoMemo📝")
col1, col2 = st.columns([7, 3])


with col1:
    generate_memo()
    tab1, tab2 = st.tabs(["🔖 タグ検索", "📝 メモ一覧"])

    # tab1 タグ検索
    with tab1:
        st.write("ここにはタグ検索を表示します。")
        search_by_tag()
    # tab2 メモ一覧表示
    with tab2:
        show_all_memos()

with col2:
    st.write("ここにはタグ一覧を表示します。")
    manage_tags()

