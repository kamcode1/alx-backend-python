import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that opens a SQLite connection, ensures the `users` table exists,
    passes the connection to the decorated function, and closes the connection afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        # Ensure users table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        conn.commit()
        result = func(conn, *args, **kwargs)
        conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by ID from the `users` table.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example call — make sure to insert some data before calling this!
user = get_user_by_id(user_id=1)
if user:
    print(f"User found: {user}")
else:
    print("No user with that ID found.")
