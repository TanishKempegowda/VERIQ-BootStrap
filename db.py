# database/db.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'veriq.db')

def get_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allows us to access columns by name
    return conn

def init_db():
    """Reads the schema.sql file and creates the tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_file, 'r') as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    init_db()