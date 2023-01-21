from src import db, APP


# @APP.cli.command('db_create')
def db_create():
    with APP.app_context():
        db.create_all()
    print("Database Created!")


def db_drop():
    db.drop_all()
    print("Database Dropped!")


if __name__ == '__main__':
    # db_drop()
    db_create()
