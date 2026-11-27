from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from io_flask_toolkit.io_db import IoModelBase


class User(IoModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(
        String(128), unique=False, nullable=False)
