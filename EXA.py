import streamlit as st

import pandas as pd


# データの初期化

if 'notes' not in st.session_state:

    st.session_state.notes = pd.DataFrame(columns=['content', 'tags'])


# サイドバー：新規メモ作成

with st.sidebar:

    st.header("新規メモ")

    note_content = st.text_area("メモ内容")

    note_tags = st.text_input("タグ（カンマ区切り）")

    if st.button("メモを追加"):

        new_note = pd.DataFrame({'content': [note_content], 'tags': [note_tags]})

        st.session_state.notes = pd.concat([st.session_state.notes, new_note], ignore_index=True)


# メインページ：メモの表示

st.title("Notionライクメモアプリ")


# タグフィルタリング

all_tags = set(tag for tags in st.session_state.notes['tags'] for tag in tags.split(',') if tag)

selected_tag = st.selectbox("タグでフィルタ", ["すべて"] + list(all_tags))


filtered_notes = st.session_state.notes

if selected_tag != "すべて":

    filtered_notes = filtered_notes[filtered_notes['tags'].str.contains(selected_tag)]


# メモの表示

for i, note in filtered_notes.iterrows():

    st.text_area(f"メモ {i+1}", note['content'], height=100)

    st.text(f"タグ: {note['tags']}")

    st.markdown("---")