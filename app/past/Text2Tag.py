# ライブラリのインポート
import os
from groq import Groq

# APIキーの取得
with open("data\Groq_key.txt") as f:
    GROQ_API_KEY = f.read()

client = Groq(
    api_key=os.environ.get(GROQ_API_KEY)
    )

# 入力テキストを設定
def TagGenerate(memo_text):
    user_input = memo_text
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
        model="llama-3.3-70b-versatile",
    )

    # 内容(タグ)を出力
    outputs = chat_completion.choices[0].message.content
    return outputs
