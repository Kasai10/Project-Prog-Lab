import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "app.db"

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    conn.close()
    result = [dict(row) for row in result]
    return result[0] if one else result
