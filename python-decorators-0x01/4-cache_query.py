import sqlite3
import functools

# Global cache dictionary
query_cache = {}

# Reuse the with_db_connection decorator from earlier
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# Implement the cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Assume query is passed as keyword arg or positional
        query = kwargs.get('query')
        if query is None and len(args) > 1:
            query = args[1]
        if query in query_cache:
            print("Returning cached result for query.")
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Query executed and result cached.")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
