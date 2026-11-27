from flask import Flask
from config import Config
from io_flask_toolkit import IoFlaskToolkit
from io_flask_toolkit.io_db import IoDatabase
from io_flask_toolkit.io_extras import IoInMemoryDatabase


db = IoDatabase()
auth_db = IoInMemoryDatabase(db_id=1)

io_flask_toolkit = IoFlaskToolkit()


def __register_blueprints(app: Flask):
    from io_flask_app import blueprints

    app.register_blueprint(blueprints.core_blueprint)


def __setup_db(app: Flask):
    from io_flask_app import models

    db.setup(app.config["DATABASE_URI"])
    db.create_all()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = "debug_secret"
    app.config.from_object(config_class)

    __setup_db(app)

    with app.app_context():
        __register_blueprints(app)
        io_flask_toolkit.init_app(app=app)

        # app.logger.info(msg="app has been created")

        return app
