from io_flask_toolkit.io_db import ModelBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

class BaseUserModel(ModelBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
