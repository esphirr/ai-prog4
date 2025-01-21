# タグを付ける処理
import os
from groq import Groq

# APIキーの取得
with open("data\Groq_key.txt") as f:
    GROQ_API_KEY = f.read()

client = Groq(
    api_key=os.environ.get(GROQ_API_KEY)
    )

# 処理
def TagSelect(memo_tag):
    user_input = memo_tag
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
                入力された文章と最も近い単語を、以下の単語リストから
                単語のみ で出力してください。
                他に余計な文字列等は生成しないでください。

                <単語リスト>
                [ゲーム,生活,メモ,勉強,料理]
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
