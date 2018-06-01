from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import Base

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
