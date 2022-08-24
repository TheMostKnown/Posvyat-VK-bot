from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from app.config import settings

# Создание движка
database = declarative_base()
engine = create_engine(settings.DB_PATH, pool_size=1000)


# Таблица с группами
class Groups(database):
    __tablename__ = 'groups'

    group_num = Column(Integer, primary_key=True)
    group_info = Column(String)


# Таблица с участниками
class Guests(database):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True)
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

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    vk_org_link = Column(String)
    group = Column(String)

# Таблица рассылок
class Sendings(database):
    __tablename__ = 'sendings'

    id = Column(String, primary_key=True)
    mail_name = Column(String, primary_key=True)
    send_time = Column(DateTime)
    group_num = Column(Integer, ForeignKey('groups', onupdate='cascade', ondelete='cascade'))
    text = Column(String)
    pics = Column(String)
    video = Column(String)
    reposts = Column(String)
    docs = Column(String)

# Таблица с инфой о посвяте
class Info(database):
    __tablename__ = 'info'

    question = Column(String, primary_key=True)
    answer = Column(String)


# Таблица с тех саппортом
class TechSupport(database):
    __tablename__ = 'tech_support'

    id = Column(Integer, primary_key=True)
    vk_link = Column(String, ForeignKey('guests.vk_link', onupdate='cascade', ondelete='cascade'))
    per_question = Column(String)
    status = Column(Boolean)


# Таблица с командами
class Command(database):
    __tablename__ = 'command'

    name = Column(String, primary_key=True)
    arguments = Column(String)
    desc = Column(String)
    admin = Column(Boolean)


# Создание таблиц
def create_tables(engine: Engine) -> None:
    database.metadata.create_all(engine)


# Создание сессии
def get_session(engine: Engine) -> Session:
    return sessionmaker(bind=engine)()


# Удаление таблиц
def delete_tables():
    Groups.__table__.drop(engine)
    Guests.__table__.drop(engine)
    Orgs.__table__.drop(engine)
    Sendings.__table__.drop(engine)
    Info.__table__.drop(engine)
    TechSupport.__table__.drop(engine)


if __name__ == "__main__":
    create_tables(engine)
