# main class
# library import
import streamlit as st
import requests
import json
from datetime import datetime
# pyfile import
from memo_class import MemoGenerate, MemoShow

API_URL = "http://localhost:8000"

# メインエリア
st.set_page_config(page_title="📝MemoMemo📝", layout="wide")
st.title("📝MemoMemo📝")

tab1, tab2 = st.tabs(["新規メモ", "メモ一覧"])
# tab1 新規メモ作成
with tab1:
    MemoGenerate()
# tab2 メモ一覧表示
with tab2:
    MemoShow()