from io_flask_toolkit.io_db import IoModelBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

class IoBaseUserModel(IoModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
