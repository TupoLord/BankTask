import requests
from bs4 import BeautifulSoup
import psycopg2
from config.config import DB_HOST, DB_NAME, DB_USER, DB_PASS
from utils.constants import DB_URL
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cursor = conn.cursor()

def check_banks():
    cursor.execute("SELECT * FROM bank")
    rez = cursor.fetchall()
    if len(rez) == 0:
        cursor.execute("TRUNCATE TABLE bank RESTART IDENTITY")
        get_bank_names()
    else:
        pass


def get_bank_names():
    list_banks = []

    url = DB_URL

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.find_all("div", class_='py-2 overflow-hidden')
    for i in data:
        name = i.find('h3').text
        list_banks.append(name)
        cursor.execute("INSERT INTO bank  (bank_name) VALUES  (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()

check_banks()
