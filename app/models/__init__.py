import psycopg2
import os
from psycopg2 import sql, extras

# 1. Gerenciador de contexto WITH
# 2. Criar uma funcao que retorne uma nova connection sempre que necessário
# 3. Utilizar herança POO para conexao


configs = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


class DatabaseConnector:
    DEC2FLOAT = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMAL.values,
        "DEC2FLOAT",
        lambda value, curs: float(value) if value is not None else None,
    )
    psycopg2.extensions.register_type(DEC2FLOAT)

    @classmethod
    def get_conn_cur(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor()
        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS animes (
                id              BIGSERIAL       PRIMARY KEY,
                anime           VARCHAR(100)    NOT NULL        UNIQUE,
                released_date   DATE            NOT NULL,
                seasons         INTEGER         NOT NULL
            );"""
        )

    @classmethod
    def commit_and_close(cls, commit=True):
        if commit:
            cls.conn.commit()
        cls.cur.close()
        cls.conn.close()

    