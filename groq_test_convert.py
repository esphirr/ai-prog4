# ライブラリのインポート
import os
from groq import Groq

# APIキーを読み込む
with open("data\Groq_key.txt") as f:
    GROQ_API_KEY = f.read()

client = Groq(
    api_key=os.environ.get(GROQ_API_KEY) # ここはtxtファイルを読み込む形が良いかも
    )


# 入力テキストを設定
user_input = input() # "こんにちは。RTAにおいて重要なのは、ゲームをクリアするまでのスピードと、画面操作を行う精度です。"

# ここで設定を行う
chat_completion = client.chat.completions.create(
    # メッセージ設定
    messages = [
        {
            # システム設定
            "role": "system",
            "content":
            '''
            入力された文章から、関連性の高いワードを5つ生成してください。
            出力形式は、 「word1, word2, word3, word4, word5」 で出力してください。
            '''
        },
        {
            # ユーザー設定
            "role": "user",
            "content": user_input
        }
    ],
    # モデル設定
    model="llama-3.3-70b-versatile",
)

# 内容を出力
outputs = chat_completion.choices[0].message.content
print(outputs)

word_list = outputs.split(",")
print(word_list)

print(word_list[2])
