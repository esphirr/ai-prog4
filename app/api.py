# FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

app = FastAPI()

# データモデル
class Memo(BaseModel):
    title: str
    tag: str
    content: str

class MemoResponse(BaseModel):
    id: int
    title: str
    tag: str
    content: str
    created_at: str

# データベース初期化
def init_db():
    conn = sqlite3.connect('memos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS memos
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT,
         tag TEXT,
         content TEXT,
         created_at TIMESTAMP)
        ''')
    conn.commit()
    conn.close()

init_db()

# メモ作成
@app.post("/memos/", response_model=MemoResponse)
def create_memo(memo: Memo):
    conn = sqlite3.connect('memos.db')
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO memos (title, tag, content, created_at) VALUES (?, ?, ?, ?)",
        (memo.title, memo.tag, memo.content, created_at)
    )
    memo_id = c.lastrowid
    conn.commit()
    conn.close()
    return MemoResponse(id=memo_id, title=memo.title, tag=memo.tag, content=memo.content, created_at=created_at)

# メモ一覧取得
@app.get("/memos/", response_model=List[MemoResponse])
def get_memos():
    conn = sqlite3.connect('memos.db')
    c = conn.cursor()
    c.execute("SELECT * FROM memos ORDER BY created_at DESC")
    memos = c.fetchall()
    conn.close()
    return [
        MemoResponse(id=memo[0], title=memo[1], tag=memo[2], content=memo[3], created_at=memo[4])
        for memo in memos
    ]

# メモ削除
@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int):
    conn = sqlite3.connect('memos.db')
    c = conn.cursor()
    c.execute("DELETE FROM memos WHERE id = ?", (memo_id,))
    conn.commit()
    conn.close()
    return {"message": "Memo deleted successfully"}