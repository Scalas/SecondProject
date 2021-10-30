import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

with open('secrete_file.json') as f:
    secretes = json.loads(f.read())

engine = create_engine('postgresql://{username}:{db_password}@{host}:{port}/{db_name}'.format(
    username='postgres',
    db_password=secretes['db_password'],
    host='localhost',
    port='5432',
    db_name='postgres'
))

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    Base.metadata.create_all(engine)
