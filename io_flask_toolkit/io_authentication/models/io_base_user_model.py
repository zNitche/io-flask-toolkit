from io_flask_toolkit.io_db import IoModelBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

class IoBaseUserModel(IoModelBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
