from flask import Flask


def register_blueprints(app: Flask):
    from io_flask_app import blueprints

    app.register_blueprint(blueprints.core_blueprint)


def create_app():
    app = Flask(__name__, instance_relative_config=False, static_folder=None)

    with app.app_context():
        register_blueprints(app)

        # app.logger.info(msg="app has been created")

        return app
