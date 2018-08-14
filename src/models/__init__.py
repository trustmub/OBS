from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker, relationship, backref
from src.models.models import BASE

engine = create_engine('sqlite:///bank_database.db')
BASE.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
