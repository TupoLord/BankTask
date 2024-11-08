from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DB_HOST, DB_NAME, DB_USER, DB_PASS
Base = declarative_base()

class Bank(Base):
    __tablename__ = 'bank'
    id = Column(Integer, primary_key=True)
    bank_name = Column(String)


class Custom(Base):
    __tablename__ = 'custom'
    id = Column(Integer, primary_key=True)
    custom_name = Column(String)
    bank_name = Column(String, ForeignKey('bank.bank_name'))
    user_id = Column(Integer)


# Класс для работы с базой данных
class Database:
    def __init__(self):
        self.engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()


class BankManager:
    def __init__(self, db: Database):
        self.db = db

    def select_bank(self, name: str, custom_bank: str, user_id: int):
        banks = self.db.session.query(Bank.bank_name).filter(Bank.bank_name.ilike(f'%{name}%')).all()
        customs = self.db.session.query(Custom.custom_name).filter(Custom.bank_name.ilike(f'%{custom_bank}%'),
                                                                   Custom.user_id == user_id).all()

        bank_names = [bank[0] for bank in banks]
        custom_names = [custom[0] for custom in customs]
        return bank_names + custom_names

    def add_custom_bank(self, custom_bank: str, name: str, user_id: int):
        new_custom = Custom(custom_name=custom_bank, bank_name=name, user_id=user_id)
        self.db.session.add(new_custom)
        self.db.commit()
