import os
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

# Database settings
class DBSettings:
    """Database configuration settings."""
    DB_PATH = Path(__file__).parent / os.getenv("DB_NAME", "orders.db")
    DB_CONNECTION_STRING = f"sqlite:///{DB_PATH}"
    TIMEOUT = float(os.getenv("DB_TIMEOUT", 5.0))
    CHECK_SAME_THREAD = os.getenv("DB_CHECK_SAME_THREAD", "false").lower() == "true"
    ISOLATION_LEVEL = os.getenv("DB_ISOLATION_LEVEL", "DEFERRED")

    @classmethod
    def __repr__(cls):
        return (f"DBSettings(path={cls.DB_PATH}, timeout={cls.TIMEOUT}, "
                f"check_same_thread={cls.CHECK_SAME_THREAD})")

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(
        DBSettings.DB_PATH,
        timeout=DBSettings.TIMEOUT,
        check_same_thread=DBSettings.CHECK_SAME_THREAD
    )
    conn.isolation_level = DBSettings.ISOLATION_LEVEL
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_context():
    """Context manager for database connections."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize the database schema."""
    with get_db_context() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                eta TEXT NOT NULL,
                carrier TEXT NOT NULL
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] == 0:
            sample_orders = [
                ("4821", "shipped", "July 30", "FedEx"),
                ("9910", "processing", "Aug 02", "UPS"),
                ("0042", "delivered", "July 25", "DHL"),
            ]
            cursor.executemany(
                "INSERT INTO orders (order_id, status, eta, carrier) VALUES (?, ?, ?, ?)",
                sample_orders
            )

def query_order(order_id: str) -> Optional[dict]:
    """Look up an order by ID. Returns a dict or None if not found."""
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

if __name__ == "__main__":
    print(f"Database Settings: {DBSettings}")
    init_db()
    print(f"Database initialized at {DBSettings.DB_PATH}")
