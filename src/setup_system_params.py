from flask import Blueprint

from src import db

cmd = Blueprint('db', __name__)  # created a Blueprint for this module


@cmd.cli.command('db-create')  # rather than generating the cli command with app,
def createDatabase():  # used the blueprint, cmd
    db.create_all()
    print('***** Datebase created ****')
