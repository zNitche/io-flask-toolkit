from io_flask_toolkit.io_extras import load_dotenv
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'io_flask_app'))

load_dotenv(".env")


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR_PATH = os.path.join(CURRENT_DIR, "io_flask_app")
    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "database", "migrations")

    LOGS_DIR_PATH = os.path.join(CURRENT_DIR, "logs")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URI = f"sqlite:////{CURRENT_DIR}/database/app.db"
