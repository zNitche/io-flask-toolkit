# most modules origin https://github.com/zNitche/IOr

from __future__ import annotations
from typing import TYPE_CHECKING
from flask import Flask

# for pylance
if TYPE_CHECKING:
    from io_flask_toolkit.io_authentication import IoAuthenticationManager


__version__ = "0.0.0"

FLASK_EXTENSION_NAME = "io_flask_toolkit"

class IoFlaskToolkit:
    def __init__(self) -> None:
        self.authentication_manager: IoAuthenticationManager | None = None

    def __setup_io_authentication(self):
        pass

    def init_app(self, app: Flask):
        app.extensions[FLASK_EXTENSION_NAME] = self
