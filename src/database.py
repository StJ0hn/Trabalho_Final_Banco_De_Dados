import psycopg2
from psycopg2 import pool
import sys

class Database:
    _pool = None

    @classmethod
    def initialize(cls):
        try:
            cls._pool = pool.SimpleConnectionPool(
                1, 10,
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432",
                database="sistema organizacional de academia"
            )
        except Exception as e:
            print(f"Fatal: Erro ao conectar no banco: {e}")
            sys.exit(1)

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize()
        return cls._pool.getconn()

    @classmethod
    def return_connection(cls, conn):
        if cls._pool and conn:
            cls._pool.putconn(conn)

    @classmethod
    def close_all(cls):
        if cls._pool:
            cls._pool.closeall()