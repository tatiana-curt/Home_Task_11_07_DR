# pip install sqlalchemy Установка библиотеки

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
import json

def auth_info_bd():
    dbname = input('Введите имя БД в которую хотите записать данные: ')
    user = input('Введите пользователся БД: ')
    password = input('Введите пароль пользователя БД: ')
    auth_unfo = f'postgresql://{user}:{password}@localhost/{dbname}'
    return auth_unfo


Base = declarative_base()
engine = create_engine(auth_info_bd())
# engine = create_engine('postgresql://postgres:123456789@localhost/test_bd')
Session = sessionmaker(bind=engine)
session = Session()

def get_top_10_person():
    with open('Top_10_person.json', 'r', encoding='utf-8') as out_info:
        top_10_person = json.load(out_info)
        return top_10_person


class VKinder(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    id_name = Column(Integer, nullable=False, unique=True)
    photos = Column(JSONB, server_default='[]', default=list, nullable=False)

def drop_all():
    Base.metadata.drop_all(engine)
# drop_all()


def create_all():
    Base.metadata.create_all(engine)
# create_all()


def add_person(**kwargs):
    person = VKinder(**kwargs)
    session.add(person)
    session.commit()


def add_persons():
    top_10_person = get_top_10_person()
    for item in top_10_person:
        add_person(id_name=item['id'],
                   photos=item['photos'])
# add_persons()

