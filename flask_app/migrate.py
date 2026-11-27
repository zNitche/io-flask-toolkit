from io_flask_toolkit.io_db import IoDatabase, migrations
from config import Config


def main():
    db = IoDatabase()
    db.setup(Config.DATABASE_URI)

    if db.engine is None:
        raise Exception("can't create database engine, exiting...")

    migrations.init_migrations("", Config.MIGRATIONS_DIR_PATH, db.engine)
    migrations.migrate(Config.MIGRATIONS_DIR_PATH, db.engine)


if __name__ == '__main__':
    main()
