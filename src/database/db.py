from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.config import Application_Config
from src.utils.logger import AppLogger

Base = declarative_base()


class Bank(Base):
    __tablename__ = "bank"
    id = Column(Integer, primary_key=True)
    bank_name = Column(String)


class Custom(Base):
    __tablename__ = "custom"
    id = Column(Integer, primary_key=True)
    custom_name = Column(String)
    bank_name = Column(String, ForeignKey("bank.bank_name"))
    user_id = Column(Integer)


# Класс для работы с базой данных
class Database:
    def __init__(self, config: Application_Config):
        self.__connection_string = lambda conn_type: f"{conn_type}://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}"
        self.engine = create_engine(self.__connection_string('postgresql'))
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.logger = AppLogger('bank_task_db').get_logger()

        self.async_engine = create_async_engine(self.__connection_string('postgresql+asyncpg'))
        self.async_session = sessionmaker(bind=self.async_engine, class_=AsyncSession, expire_on_commit=False)

    async def async_session(self):
        async with self.async_session() as session:
            yield session


    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()

    async def close_async_session(self):
        self.async_session.close_all()

    async def commit_async(self, session: AsyncSession):
        await session.commit()


class BankManager:
    def __init__(self, db: Database):
        self.db = db

    def select_bank(self, name: str, custom_bank: str, user_id: int):
        banks = (
            self.db.session.query(Bank.bank_name)
            .filter(Bank.bank_name.ilike(f"%{name}%"))
            .all()
        )
        customs = (
            self.db.session.query(Custom.custom_name)
            .filter(
                Custom.bank_name.ilike(f"%{custom_bank}%"), Custom.user_id == user_id
            )
            .all()
        )

        bank_names = [bank[0] for bank in banks]
        custom_names = [custom[0] for custom in customs]
        return bank_names + custom_names

    def add_custom_bank(self, custom_bank: str, name: str, user_id: int):
        new_custom = Custom(custom_name=custom_bank, bank_name=name, user_id=user_id)
        self.db.session.add(new_custom)
        self.db.commit()

