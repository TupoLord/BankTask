import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

list_banks_1 = []
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cursor = conn.cursor()

def select_bank(name):
    cursor.execute("SELECT bank_name FROM bank WHERE bank_name LIKE %s", ('%' + name + '%',))
    rez = cursor.fetchall()
    conn.commit()
    return rez


def add_new_bank(new_bank):
    cursor.execute("INSERT INTO bank (bank_name) VALUES (%s)", (new_bank,))
    conn.commit()


def add_custom_bank(custom_bank, name, id):
    cursor.execute("INSERT INTO custom (custom_name, bank_name, user_id) VALUES (%s, %s, %s)", (custom_bank, name, id))
    conn.commit()

def return_custom_bank(custom_bank, id):
    cursor.execute("SELECT custom_name FROM custom WHERE bank_name LIKE %s AND user_id = %s", ('%' + custom_bank + '%', id))
    rez = cursor.fetchall()
    return rez
