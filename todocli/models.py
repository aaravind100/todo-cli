"""Models for todo database table."""
from sqlalchemy import Boolean, Column, Integer, String

from todocli.base import Base
from todocli.config import Icons


class Todo(Base):
    """Todo item model."""
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=100))
    check = Column(Boolean, default=False)

    def __init__(self, title: str, check: bool = False) -> None:
        """Init function.

        :param title: todo title
        :type title: str
        :param check: todo status, defaults to False
        :type check: bool, optional
        """
        self.title = title
        self.check = check

    def __str__(self) -> str:
        """String representation.

        :return: string representation of todo item
        :rtype: str
        """
        return f'{self.id} | {self.title} | {self.check_icon}'

    @property
    def check_icon(self) -> str:
        """Helper method for getting status emoji.

        :return: status emoji
        :rtype: str
        """
        return Icons.CHECK.value if self.check else Icons.UNCHECK.value
