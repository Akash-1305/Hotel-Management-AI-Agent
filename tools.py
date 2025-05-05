import os
import sqlite3
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("SQLITE_DB_PATH")

def run_query(query: str, params: tuple = ()) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

@tool("read_records", parse_docstring=True)
def read_records(table: str, condition: str = "", limit: int = 5) -> list:
    """Read rows from a table.

    Args:
        table: Table name (e.g., 'Rooms', 'Bookings').
        condition: Optional WHERE clause (e.g., "isVacant = 1").
        limit: Max number of rows to fetch.
    """
    q = f"SELECT * FROM {table}"
    if condition:
        q += f" WHERE {condition}"
    q += f" LIMIT ?"
    return run_query(q, (limit,))

@tool("describe_table", parse_docstring=True)
def describe_table(table: str) -> list:
    """Get table structure and columns.

    Args:
        table: Table name to describe.
    """
    q = f"PRAGMA table_info({table});"
    return run_query(q)

@tool("custom_query", parse_docstring=True)
def custom_query(query: str) -> list:
    """Run a custom SQL SELECT query (read-only).

    Args:
        query: A safe SELECT query to execute.
    """
    if not query.strip().lower().startswith("select"):
        return [{"error": "Only SELECT queries are allowed"}]
    return run_query(query)
