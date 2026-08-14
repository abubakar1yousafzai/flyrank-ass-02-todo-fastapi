import sqlite3

def get_connection():
    return sqlite3.connect("tasks.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL
        )
"""
)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title , done) VALUES (? , ?)",
            [
                ("Buy milk", False),
                ("clean room", False),
                ("Finish assignment", True)
            ]
        )

    
    conn.commit()
    conn.close()
