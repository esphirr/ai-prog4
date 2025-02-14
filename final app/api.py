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

class Tag(BaseModel):
    name: str

class TagResponse(BaseModel):
    id: int
    name: str

# データベース初期化
def init_db():
    conn = sqlite3.connect('memo_system.db')
    c = conn.cursor()
    # memosテーブルの作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS memos
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT,
         tag TEXT,
         content TEXT,
         created_at TIMESTAMP)
        ''')
    # tagsテーブルの作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS tags
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT UNIQUE)
        ''')
    conn.commit()
    conn.close()

init_db()
# def init_db():
#     conn = sqlite3.connect('memo_system.db')
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS memos
#         (id INTEGER PRIMARY KEY AUTOINCREMENT,
#          title TEXT,
#          tag TEXT,
#          content TEXT,
#          created_at TIMESTAMP)
#         ''')
#     conn.commit()
#     conn.close()

# init_db()
# ------------------------------------------------------------
# メモ作成
@app.post("/memos/", response_model=MemoResponse)
def create_memo(memo: Memo):
    conn = sqlite3.connect('memo_system.db')
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
    conn = sqlite3.connect('memo_system.db')
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
    conn = sqlite3.connect('memo_system.db')
    c = conn.cursor()
    c.execute("DELETE FROM memos WHERE id = ?", (memo_id,))
    conn.commit()
    conn.close()
    return {"message": "Memo deleted successfully"}

# メモの編集
@app.put("/memos/{memo_id}", response_model=MemoResponse)
def update_memo(memo_id: int, memo: Memo):
    conn = sqlite3.connect('memo_system.db')
    c = conn.cursor()
    
    # メモの存在確認
    c.execute("SELECT * FROM memos WHERE id = ?", (memo_id,))
    if not c.fetchone():
        raise HTTPException(status_code=404, detail="Memo not found")
    
    # メモの更新
    c.execute(
        "UPDATE memos SET title = ?, tag = ?, content = ? WHERE id = ?",
        (memo.title, memo.tag, memo.content, memo_id)
    )
    
    # 更新されたメモの取得
    c.execute("SELECT * FROM memos WHERE id = ?", (memo_id,))
    updated_memo = c.fetchone()
    
    conn.commit()
    conn.close()
    
    return MemoResponse(
        id=updated_memo[0],
        title=updated_memo[1],
        tag=updated_memo[2],
        content=updated_memo[3],
        created_at=updated_memo[4]
    )

# メモの検索
# タグ検索
@app.get("/memos/tag/{tag}", response_model=List[MemoResponse])
def search_by_tag(tag: str):
    with sqlite3.connect('memo_system.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM memos WHERE tag = ? ORDER BY created_at DESC", (tag,))
        return [
            MemoResponse(
                id=memo[0],
                title=memo[1],
                tag=memo[2],
                content=memo[3],
                created_at=memo[4]
            )
            for memo in c.fetchall()
        ]

# 単語検索
@app.get("/memos/search", response_model=List[MemoResponse])
def search_memos(search_term: str):
    with sqlite3.connect('memo_system.db') as conn:
        c = conn.cursor()
        search_pattern = f"%{search_term}%"
        c.execute("""
            SELECT * FROM memos 
            WHERE title LIKE ? OR content LIKE ? 
            ORDER BY created_at DESC
            """, 
            (search_pattern, search_pattern))
        return [
            MemoResponse(
                id=memo[0],
                title=memo[1],
                tag=memo[2],
                content=memo[3],
                created_at=memo[4]
            )
            for memo in c.fetchall()
        ]
# ------------------------------------------------------------
# タグ管理
# タグの作成
@app.post("/tags/", response_model=TagResponse)
def create_tag(tag :Tag):
    conn = sqlite3.connect('memo_system.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO tags (name) VALUES (?)",
        (tag.name,)
    )
    tag_id = c.lastrowid
    conn.commit()
    conn.close()
    return TagResponse(id=tag_id, name=tag.name)

# タグ一覧の取得
@app.get("/tags/", response_model=List[TagResponse])
def get_tags():
    conn = sqlite3.connect('memo_system.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM tags")
    tags = c.fetchall()
    conn.close()
    return [
        TagResponse(id=tag[0], name=tag[1])
        for tag in tags
    ]

@app.delete("/tags/{tag_id}", response_model=List[TagResponse])
def delete_tags(tag_id :int):
    conn = sqlite3.connect('memo_system.db')
    c = conn.cursor()
    # c.execute("SELECT id, name FROM tags")
    c.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    tags = c.fetchall()
    conn.close()
    return [
        TagResponse(id=tag[0], name=tag[1])
        for tag in tags
    ]