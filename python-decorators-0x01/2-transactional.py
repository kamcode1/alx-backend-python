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


def transactional(func):
    """
    Decorator that wraps a database operation in a transaction.
    Commits if successful, rolls back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email by ID.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    if cursor.rowcount == 0:
        raise ValueError("No user found with the given ID.")
    print(f"Updated user {user_id}'s email to {new_email}.")


# Example usage
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
