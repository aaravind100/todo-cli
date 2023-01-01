"""Views for todo model."""
from dataclasses import dataclass
from typing import Iterable, Optional

from sqlalchemy.orm import Session

from todocli.models import Todo


@dataclass
class TodoView:
    """Views for Todo class.

    :param session: sql alchemy db session
    :type session: Session
    """
    session: Session

    def add_todo(self, title: str, check: bool = False) -> None:
        """Add todo items.

        :param title: todo title
        :type title: str
        :param check: todo status, defaults to False
        :type check: bool, optional
        """

        todo = Todo(title, check)
        self.session.add(todo)
        self.session.commit()
        self.session.close()

    def list_todo(self, indexes: Optional[int | list[int]] = None) -> None:
        """List todo items.

        :param indexes: todo item id, defaults to None
        :type indexes: Optional[int  |  list[int]], optional
        """

        if isinstance(indexes, int):  # one item
            todo = self.session.query(Todo).get(indexes)
            if todo:
                print('\nid | title | status')
                print('-------------------')
                print(todo)
                print('\n')
            else:
                print(f'{indexes} not found!!')
        else:
            if isinstance(indexes, list):  # many items
                todos: Iterable[Todo] = self.session.query(
                    Todo).filter(Todo.id.in_(indexes)).all()
            else:  # all items
                todos: Iterable[Todo] = self.session.query(Todo).all()
            print('\nid | title | status')
            print('-------------------')
            for todo in todos:
                print(todo)
            print('\n')
        self.session.close()

    def update_todo(
        self,
        index: int,
        title: Optional[str] = None,
        check: Optional[bool] = None
    ) -> None:
        """Update todo items.

        :param index: todo item id
        :type index: int
        :param title: todo title, defaults to None
        :type title: str, optional
        :param check: todo status, defaults to None
        :type check: Optional[bool], optional
        """

        todo: Todo = self.session.query(Todo).get(index)
        if todo:
            if title is not None:
                todo.title = title
            if check is not None:
                todo.check = check
            self.session.commit()
        else:
            print(f'{index} not found!!')
        self.session.close()

    def update_todo_check_many(
        self,
        indexes: list[int],
        check: Optional[bool] = None
    ) -> None:
        """Update status of many todo items.

        :param indexes: todo item id
        :type indexes: list[int]
        :param check: todo status, defaults to None
        :type check: Optional[bool], optional
        """

        if check is not None:
            todos: Iterable[Todo] = self.session.query(
                Todo).filter(Todo.id.in_(indexes)).all()
            for todo in todos:
                todo.check = check
            self.session.commit()
        self.session.close()

    def update_todo_all(self, check: Optional[bool] = None) -> None:
        """Update status of all todo items.

        :param check: todo status, defaults to None
        :type check: Optional[bool], optional
        """

        if check is not None:
            todos: Iterable[Todo] = self.session.query(Todo).all()
            for todo in todos:
                todo.check = check
            self.session.commit()
        self.session.close()

    def delete_todo(self, indexes: int | list[int]) -> None:
        """Delete todo items.

        :param indexes: todo item id
        :type indexes: int | list[int]
        """

        if isinstance(indexes, int):
            todo: Todo = self.session.query(Todo).get(indexes)
            if todo:
                self.session.delete(todo)
                self.session.commit()
            else:
                print(f'{indexes} not found!!')
        else:
            todos: Iterable[Todo] = self.session.query(
                Todo).filter(Todo.id.in_(indexes)).all()
            if todos:
                for todo in todos:
                    self.session.delete(todo)
                self.session.commit()
            else:
                print(f'{indexes} not found!!')
        self.session.close()

    def delete_todo_all(self) -> None:
        """Delete all todo items."""

        self.session.query(Todo).delete()
        self.session.commit()
        self.session.close()
