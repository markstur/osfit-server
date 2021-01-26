
import os

from sqlalchemy import *

engine = None
call_me_insert = None
crawl_me_insert = None

user = os.environ.get('DB_USERNAME')
passwd = os.environ.get('DB_PASSWORD')
database = os.environ.get('DB_DATABASE')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

if user and passwd and database and host and port:
    metadata = MetaData()

    call_me = Table('CALL_ME', metadata,
                    Column('PHONE', String(20)),
                    Column('POSTED', DateTime),
                    Column('CALLED', DateTime),
                    Column('STATUS', Integer))

    call_me_insert = call_me.insert()

    crawl_me = Table('CRAWL_ME', metadata,
                     Column('URL', String(2048)),
                     Column('PARENT_URL', String(2048)),
                     Column('POSTED', DateTime),
                     Column('DEPTH', Integer),
                     Column('CRAWLED', DateTime),
                     Column('STATUS', Integer))

    crawl_me_insert = crawl_me.insert()

    connection_str = f'db2+ibm_db://{user}:{passwd}@{host}:{port}/{database}'
    engine = create_engine(connection_str, echo=True)
    metadata.create_all(engine)
else:
    print("Skipping DB:  Missing config")


def insert_call_me(values):
    if engine:
        with engine.connect() as conn:
            conn.execute(call_me_insert, values)


def insert_crawl_me(values):
    if engine:
        with engine.connect() as conn:
            conn.execute(crawl_me_insert, values)
