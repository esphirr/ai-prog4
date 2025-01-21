# メインファイル
# ライブラリ インポート
import streamlit as st
# ファイル インポート
from Text2Tag import TagGenerate
from Tag2Tag import TagSelect

# タイトルとヘッダー
st.title("📝シンプルメモアプリ📝")
st.markdown("### 新規メモを追加")

# メモ部分
memo_content = st.text_area("内容")
if memo_content:
    memo_tag = TagGenerate(memo_content)
    memo_tag = TagSelect(memo_content)

# 出力部分
if st.button("保存"):
    st.markdown("**＜メモ内容＞**")
    st.markdown(memo_content)
    st.markdown("**＜今回のタグ＞**")
    st.write(memo_tag)


# 例文１
# こんにちは。RTAにおいて重要なのは、ゲームをクリアするまでのスピードと、画面操作を行う精度です。

# 例文２
# 今日の材料
# ・なす
# ・ひき肉
# ・カレー粉
