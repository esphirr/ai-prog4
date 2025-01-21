import streamlit as st
import requests
import json
from datetime import datetime
from Text2Tag import WordGenerate, TagSelect

API_URL = "http://localhost:8000"

# 新規メモ作成
def MemoGenerate():
    st.header("新規メモ作成")
    memo_title = st.text_input("タイトル")
    memo_content = st.text_area("内容")
    memo_tag = WordGenerate(memo_content)
    memo_tag = TagSelect(memo_tag)

    if st.button("メモを保存"):
        if memo_title and memo_content:
            response = requests.post(
                f"{API_URL}/memos/",
                json={"title": memo_title, "tag": memo_tag, "content": memo_content}
            )
            if response.status_code == 200:
                st.success("メモを保存しました！")
            else:
                st.error("保存に失敗しました")

# メモ一覧表示
def MemoShow():
    st.header("メモ一覧")

    try:
        response = requests.get(f"{API_URL}/memos/")
        if response.status_code == 200:
            memos = response.json()

            for memo in memos:
                with st.expander(f"📝 {memo['title']} - {memo['created_at']}"):
                    st.write(memo['content'])
                    st.markdown(f"**Tag : {memo['tag']}**")
                    if st.button("削除", key=f"delete_{memo['id']}"):
                        delete_response = requests.delete(f"{API_URL}/memos/{memo['id']}")
                        if delete_response.status_code == 200:
                            st.success("メモを削除しました")
                            st.experimental_rerun()

    except requests.exceptions.ConnectionError:
        st.error("APIサーバーに接続できません。サーバーが起動しているか確認してください。")