from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from config import settings

# Создание движка
database = declarative_base()
engine = create_engine(settings.DB_PATH, pool_size=1000)


# Таблица с группами
class Groups(database):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_num = Column(Integer)
    group_info = Column(String)


# Таблица с участниками
class Guests(database):
    __tablename__ = 'guests'

    chat_id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone_number = Column(String)
    tag = Column(String)
    vk_link = Column(String, unique=True)
    groups = Column(String)
    texts = Column(String)


# Таблица с оргами
class Orgs(database):
    __tablename__ = 'orgs'

    chat_id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    vk_link = Column(String)
    groups = Column(String)


# Таблица рассылок
class Sendings(database):
    __tablename__ = 'sendings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mail_name = Column(String, unique=True)
    text = Column(String)
    groups = Column(String)
    send_time = Column(DateTime, nullable=True)
    pics = Column(String, nullable=True)
    video = Column(String, nullable=True)
    reposts = Column(String, nullable=True)
    docs = Column(String, nullable=True)


# Таблица для хранения таймера автообновления парсера
class UpdateTimer(database):
    __tablename__ = 'timer'

    update_timer = Column(Integer, primary_key=True)


# Таблица с инфой о посвяте
class Info(database):
    __tablename__ = 'info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    answer = Column(String)


# Таблица с тех саппортом
class TechSupport(database):
    __tablename__ = 'tech_support'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_link = Column(String, ForeignKey('guests.vk_link', onupdate='cascade', ondelete='cascade'))
    per_question = Column(String)
    status = Column(String)


# Таблица с командами
class Command(database):
    __tablename__ = 'command'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    arguments = Column(String)
    desc = Column(String)
    admin = Column(Boolean)


# Таблица с уведомлениями о повышении уровня
class Notifications(database):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_num = Column(Integer)
    desc = Column(String)


# Создание сессии
def get_session(engine: Engine) -> Session:
    return sessionmaker(bind=engine)()

