import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../sqls/dev.sqlite3')

class UserModel:
    @staticmethod
    def init_db():
        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER
                )
            ''')
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_user(id, name, age):
        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (id, name, age))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_all_users():
        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            return cur.fetchall()
        finally:
            conn.close()
