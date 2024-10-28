# Переименовать в db.py
# Переписать на классы
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
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
    conn.commit()
