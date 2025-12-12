"""
Database connection manager with connection pooling
"""

import mysql.connector
from mysql.connector import pooling
from config.settings import Settings

class Database:
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            self._pool = pooling.MySQLConnectionPool(
                pool_name="zoo_pool",
                pool_size=5,
                host=Settings.DB_HOST,
                port=Settings.DB_PORT,
                database=Settings.DB_NAME,
                user=Settings.DB_USER,
                password=Settings.DB_PASSWORD
            )
            print("✓ Database connection pool initialized")
        except mysql.connector.Error as e:
            print(f"✗ Database connection failed: {e}")
            raise
    
    def get_connection(self):
        """Get connection from pool"""
        try:
            return self._pool.get_connection()
        except mysql.connector.Error as e:
            print(f"Error getting connection: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query with automatic connection management"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                return cursor.lastrowid
        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            print(f"Query error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()