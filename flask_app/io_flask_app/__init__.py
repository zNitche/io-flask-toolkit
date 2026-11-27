from flask import Flask
from config import Config
from io_flask_toolkit import IoFlaskToolkit


io_flask_toolkit = IoFlaskToolkit()


def register_blueprints(app: Flask):
    from io_flask_app import blueprints

    app.register_blueprint(blueprints.core_blueprint)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = "debug_secret"
    app.config.from_object(config_class)

    with app.app_context():
        register_blueprints(app)
        io_flask_toolkit.init_app(app=app)

        # app.logger.info(msg="app has been created")

        return app
