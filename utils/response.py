import requests
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from utils.constants import DB_URL

Base = declarative_base()


class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True)
    bank_name = Column(String)


def check_banks(session):
    if session.query(Bank).count() == 0:
        session.execute(text("ALTER SEQUENCE bank_id_seq RESTART WITH 1"))
        get_bank_names(session)


def get_bank_names(session):
    list_banks = []
    url = DB_URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find_all("div", class_="py-2 overflow-hidden")

    for i in data:
        name = i.find("h3").text
        list_banks.append(name)
        new_bank = Bank(bank_name=name)
        session.add(new_bank)

    session.commit()
