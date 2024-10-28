import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def fetchall(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query, params):
        self.cursor.execute(query, params)

class BankManager:
    def __init__(self, db: Database):
        self.db = db

    def select_bank(self, name: str, custom_bank: str, user_id: int):
        query_banks = "SELECT bank_name FROM bank WHERE bank_name LIKE %s"
        banks = self.db.fetchall(query_banks, ('%' + name + '%',))

        query_customs = "SELECT custom_name FROM custom WHERE bank_name LIKE %s AND user_id = %s"
        customs = self.db.fetchall(query_customs, ('%' + custom_bank + '%', user_id))

        return banks + customs

    def add_custom_bank(self, custom_bank: str, name: str, user_id: int):
        query = "INSERT INTO custom (custom_name, bank_name, user_id) VALUES (%s, %s, %s)"
        self.db.execute(query, (custom_bank, name, user_id))
        self.db.commit()

























'''conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cursor = conn.cursor()

def select_bank(name: str, custom_bank, id):
    cursor.execute("SELECT bank_name FROM bank WHERE bank_name LIKE %s", ('%' + name + '%',))
    rez = cursor.fetchall()
    cursor.execute("SELECT custom_name FROM custom WHERE bank_name LIKE %s AND user_id = %s", ('%' + custom_bank + '%', id))
    rez1 = cursor.fetchall()
    res = rez + rez1
    conn.commit()
    return res

def add_custom_bank(custom_bank, name, id):
    cursor.execute("INSERT INTO custom (custom_name, bank_name, user_id) VALUES (%s, %s, %s)", (custom_bank, name, id))
    conn.commit()'''
