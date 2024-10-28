import requests
from bs4 import BeautifulSoup
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

def db_connect():
    list_banks = []
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor()

    url = 'https://bincheck.io/ru/RU' # Вынести в константы

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


