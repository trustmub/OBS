from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker, relationship, backref
from src.models.models import BASE
import pymysql
pymysql.install_as_MySQLdb()

# from src import APP

""" for connection to the MySQL datagase a driver needs to be installed and included ont he connection strings"""

# engine = create_engine("mysql://admin:password@database:33060/bank_database", encoding='latin1', echo=True)
engine = create_engine("mysql+pymysql://root:password@database:3306/bank_database", encoding='latin1', echo=True)
# engine = create_engine("mysql+mysqldb://admin:password@database:33060/bank_database", encoding='latin1', echo=True)
# engine = create_engine('sqlite:///bank_database.db')
BASE.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
