import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_dir = os.path.join(os.getcwd(), 'db')
db_path = os.path.join(db_dir, "database.db")
if not os.path.exists(db_dir):
    os.mkdir(db_dir)
print("database at: {}".format(db_path))
engine = create_engine('sqlite:///{}?check_same_thread=False'.format(db_path), )
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_all():
    global Base, engine
    Base.metadata.create_all(engine)
