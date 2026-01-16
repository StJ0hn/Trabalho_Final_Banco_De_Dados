import psycopg2
from psycopg2 import pool
import sys

class Database:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        try:
            #configuração do pool de conexões

            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432",
                database="sistema organizacional de academia"      # Nome do banco que criamos no pgAdmin
            )
            print("[SISTEMA] Pool de conexões iniciado com sucesso.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"[ERRO CRÍTICO] Falha ao conectar no PostgreSQL: {error}")
            sys.exit(1)

    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            cls.initialize()
        return cls._connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        if cls._connection_pool:
            cls._connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        if cls._connection_pool:
            cls._connection_pool.closeall()
            print("[SISTEMA] Conexões encerradas.")