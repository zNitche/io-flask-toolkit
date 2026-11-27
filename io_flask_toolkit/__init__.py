# most modules origin https://github.com/zNitche/IOr
from flask import Flask

__version__ = "0.0.0"

FLASK_EXTENSION_NAME = "io_flask_toolkit"

class IoFlaskToolkit:
    def __init__(self) -> None:
        pass

    def init_app(self, app: Flask):
        app.extensions[FLASK_EXTENSION_NAME].authentication_manager = None
