import mysql.connector
from mysql.connector import pooling
from .config import DB_CONFIG

pool = pooling.MySQLConnectionPool(
    pool_name="zoo_pool",
    pool_size=5,
    **DB_CONFIG
)

def get_conn():
    return pool.get_connection()

def query(sql, params=None, fetchone=False):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        if cur.with_rows:
            return cur.fetchone() if fetchone else cur.fetchall()
        conn.commit()
        return None
    finally:
        cur.close()
        conn.close()