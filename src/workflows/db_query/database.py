import sqlite3
from typing import List, Dict, Any


def get_all_tables(db_path: str) -> List[str]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


def get_table_schema(db_path: str, table_name: str) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    conn.close()
    
    schema_str = f"Table: {table_name}\nColumns:\n"
    for col in columns:
        col_name, col_type = col[1], col[2]
        schema_str += f"  - {col_name} ({col_type})\n"
    
    return schema_str


def execute_query(db_path: str, sql: str) -> List[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        conn.close()
        return result
    except Exception as e:
        return [{"error": str(e)}]
