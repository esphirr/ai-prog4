import streamlit as st
import requests
import json
from datetime import datetime

from config import API_URL
from Text2Tag import generate_word, select_tags
from utils import get_tag_list

tag_list = get_tag_list()

# 新規メモ作成
def generate_memo():
    st.subheader("新規メモ作成")
    memo_title = st.text_input("タイトル")
    memo_content = st.text_area("内容")
    generated_word = generate_word(memo_title, memo_content)
    memo_tag = select_tags(generated_word)

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
def show_all_memos():
    try:
        response = requests.get(f"{API_URL}/memos/")
        if response.status_code == 200:
            memos = response.json()

            for memo in memos:
                with st.expander(f"📝 {memo['title']} - {memo['created_at']}"):
                    st.write(memo['content'])
                    st.markdown(f"**Tag : {memo['tag']}**")
                    if st.button("削除", key=f"delete_all_{memo['id']}"):
                        delete_response = requests.delete(f"{API_URL}/memos/{memo['id']}")
                        if delete_response.status_code == 200:
                            st.success("メモを削除しました")
                            st.rerun()

    except requests.exceptions.ConnectionError:
        st.error("APIサーバーに接続できません。サーバーが起動しているか確認してください。")

def search_by_tag():
    search_term = st.pills(
        "タグを選択してください",
        options=tag_list,
        )
    
    if search_term is not None:
        try:
            response = requests.get(f"{API_URL}/memos/tag/{search_term}")
            if response.status_code == 200:
                memos = response.json()
                for memo in memos:
                    with st.expander(f"📝 {memo['title']} - {memo['created_at']}"):
                        st.write(memo['content'])
                        st.markdown(f"**Tag: {memo['tag']}**")
                        # 削除プロセス
                        if st.button("削除", key=f"delete_search_{memo['id']}"):
                            delete_response = requests.delete(f"{API_URL}/memos/{memo['id']}")
                            if delete_response.status_code == 200:
                                st.success("メモを削除しました")
                                st.rerun()

        except requests.exceptions.ConnectionError:
            st.error("APIサーバーに接続できません。サーバーが起動しているか確認してください。")

def search_by_keyword(tag_list):
    # search_term = st.multiselect(
    #     "タグを選択してください",
    #     options=tag_list,
    #     default=None
    #     )
    # if st.button("キーワード検索"):
    #     try:
    #         response = requests.get(f"{API_URL}/memos/search?search_term={search_term}")
    #         if response.status_code == 200:
    #             memos = response.json()
    #             for memo in memos:
    #                 with st.expander(f"📝 {memo['title']}"):
    #                     st.write(memo['content'])
    #                     st.markdown(f"**Tag: {memo['tag']}**")
    #                     st.text(f"作成日時: {memo['created_at']}")
    #     except requests.exceptions.ConnectionError:
    #         st.error("APIサーバーに接続できません")
    st.write("キーワード検索")



# 新規タグの作成
def manage_tags():
    st.subheader("新規タグの作成")
    new_tag_name = st.text_input("タグ名")

    if st.button("タグを作成"):
        if new_tag_name:
            response = requests.post(f"{API_URL}/tags/", json={"name": new_tag_name})
            if response.status_code == 200:
                st.success("タグを作成しました！")
                st.rerun()
            else:
                st.error("タグの作成に失敗しました")

    # タグ一覧の取得と表示
    st.markdown(f"**🔖 タグ一覧**")

    response = requests.get(f"{API_URL}/tags/")
    if response.status_code == 200:
        tags = response.json()

        for tag in tags:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{tag['name']}**")
            with col2:
                if st.button("削除", key=f"delete_tag_{tag['id']}"):
                    delete_response = requests.delete(f"{API_URL}/tags/{tag['id']}")
                    if delete_response.status_code == 200:
                        st.success("タグを削除しました")
                        st.rerun()