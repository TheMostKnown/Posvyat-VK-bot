from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from vk_config import db_path


# Создание движка
database = declarative_base()
engine = create_engine(db_path, pool_size=1000)


# Таблица с группами
class groups(database):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_info = Column(String)


# Таблица с участниками
class guests(database):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone_number = Column(String)
    tag = Column(String)
    vk_link = Column(String, unique=True)
    first_group = Column(Boolean)
    second_group = Column(Boolean)
    third_group = Column(Boolean)
    fourth_group = Column(Boolean)
    fifth_group = Column(Boolean)
    sixth_group = Column(Boolean)
    seventh_group = Column(Boolean)
    eighth_group = Column(Boolean)
    ninth_group = Column(Boolean)
    tenth_group = Column(Boolean)
    eleventh_grup = Column(Boolean)
    twelfth_group = Column(Boolean)
    thirteenth_group = Column(Boolean)


# Таблица с оргами
class orgs(database):
    __tablename__ = 'orgs'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    vk_org_link = Column(String)
    first_org_group = Column(Boolean)
    second_org_group = Column(Boolean)



# Таблица рассылок
class sendings(database):
    __tablename__ = 'sendings'

    mail_name = Column(String, primary_key=True)
    send_time = Column(DateTime)
    group_num = Column(Integer, ForeignKey('groups', onupdate='cascade', ondelete='cascade'))
    text = Column(String)
    media = Column(String)



# Таблица с инфой о посвяте
class info(database):
    __tablename__ = 'info'

    question = Column(String, primary_key=True)
    answer = Column(String)


# Таблица с тех саппортом
class tech_support(database):
    __tablename__ = 'tech_support'

    id = Column(Integer, primary_key=True)
    vk_link = Column(String, ForeignKey('guests.vk_link', onupdate='cascade', ondelete='cascade'))
    per_question = Column(String)
    status = Column(Boolean)


# Создание таблиц
def create_tables(engine: Engine) -> None:
    database.metadata.create_all(engine)


# Создание сессии
def get_session(engine: Engine) -> Session:
    return sessionmaker(bind=engine)()


# Удаление таблиц
def delete_tables():
    groups.__table__.drop(engine)
    guests.__table__.drop(engine)
    orgs.__table__.drop(engine)
    sendings.__table__.drop(engine)
    info.__table__.drop(engine)
    tech_support.__table__.drop(engine)


if __name__ == "__main__":
    create_tables(engine)
