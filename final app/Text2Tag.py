# ライブラリのインポート
import os
from groq import Groq
from config import Groq_model
from utils import get_tag_list

# APIキーの取得
with open("data\Groq_key.txt") as f:
    GROQ_API_KEY = f.read()

client = Groq(
    api_key=os.environ.get(GROQ_API_KEY)
    )

tag_list = get_tag_list()

# 入力テキストを設定
def generate_word(memo_title, memo_text):
    user_input = f'''
    タイトル：
    {memo_title}
    メモの内容：
    {memo_text}
    '''
    # user_input = "こんにちは。RTAにおいて重要なのは、ゲームをクリアするまでのスピードと、画面操作を行う精度です。"

    # ここで設定を行う
    chat_completion = client.chat.completions.create(
        # メッセージ設定
        messages = [
            {
                # システム設定（具体的な出力の指示とか）
                "role": "system",
                "content":
                # プロンプト
                '''
                入力された文章から、関連性の高いワードを1つ生成してください。
                1単語のみ で出力してください。
                他に余計な文字列等は生成しないでください。
                '''
            },
            {
                # ユーザー設定
                "role": "user",
                "content": user_input
            }
        ],
        # モデル設定
        model=Groq_model,
    )
    # 内容(タグ)を出力
    outputs = chat_completion.choices[0].message.content
    return outputs

def select_tags(generated_word):
    user_input = generated_word
    # user_input = "こんにちは。RTAにおいて重要なのは、ゲームをクリアするまでのスピードと、画面操作を行う精度です。"
    # ここで設定を行う
    chat_completion = client.chat.completions.create(
        # メッセージ設定
        messages = [
            {
                # システム設定（具体的な出力の指示とか）
                "role": "system",
                "content":
                # プロンプト
                f'''
                入力された文章と最も近い単語を、以下の単語リストから
                単語のみ で出力してください。
                他に余計な文字列等は生成しないでください。

                <単語リスト>
                {tag_list}
                '''
            },
            {
                # ユーザー設定
                "role": "user",
                "content": user_input
            }
        ],
        # モデル設定
        model=Groq_model,
    )
    # 内容(タグ)を出力
    outputs = chat_completion.choices[0].message.content
    return outputs
