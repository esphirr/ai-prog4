import requests
from config import API_URL

def get_tag_list():
    """tagsテーブルからタグリストを取得する"""
    response = requests.get(f"{API_URL}/tags/")
    if response.status_code == 200:
        tags = response.json()
        return [tag['name'] for tag in tags]
    return []  # エラー時は空リストを返す