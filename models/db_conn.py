from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import BASE

engine = create_engine('sqlite:///bank_database.db')
BASE.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
