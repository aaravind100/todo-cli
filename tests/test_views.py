"""Test todo views"""
from typing import Iterable, Tuple

import pytest
from pytest import CaptureFixture
from sqlalchemy.orm import Session

from todocli.models import Todo
from todocli.views import TodoView


@pytest.mark.usefixtures('session')
@pytest.mark.parametrize(
    ('inputs', 'expected', 'index'),
    ((('hello', False), Todo('hello', False), 1),
     (('world', ), Todo('world', ), 2)))
def test_add_todo(session: Session,
                  inputs: Tuple[str,
                                bool],
                  expected: Todo,
                  index: int) -> None:
    """Test add todo.

    :param session: sql alchemy db session
    :type session: Session
    :param inputs: test input
    :type inputs: Tuple[str, bool]
    :param expected: expected output
    :type expected: Todo
    :param index: index for test item
    :type index: int
    """

    todo_view = TodoView(session)
    todo_view.add_todo(*inputs)
    todo: Todo = session.query(Todo).get(index)
    assert expected.title == todo.title
    assert expected.check == todo.check


@pytest.mark.usefixtures('session', 'capsys')
def test_list_todo(session: Session, capsys: CaptureFixture) -> None:
    """Test list todo.

    :param session: sql alchemy db session
    :type session: Session
    """

    test_out_1: str = """
id | title | status
-------------------
1 | hello world | ❌


"""
    test_out_2: str = """
id | title | status
-------------------
1 | hello world | ❌
2 | meh | ✅


"""
    test_out_not_found: str = '100 not found!!\n'

    todo_view = TodoView(session)
    todo_view.delete_todo_all()
    todo_view.add_todo('hello world')
    todo_view.list_todo()
    out, _ = capsys.readouterr()

    assert out == test_out_1

    todo_view.add_todo('meh', True)
    todo_view.list_todo()
    out, _ = capsys.readouterr()
    assert out == test_out_2

    todo_view.list_todo(1)
    out, _ = capsys.readouterr()
    assert out == test_out_1

    todo_view.add_todo('meh 2')
    todo_view.list_todo([1, 2])
    out, _ = capsys.readouterr()
    assert out == test_out_2

    todo_view.list_todo(100)
    out, _ = capsys.readouterr()
    assert out == test_out_not_found


@pytest.mark.usefixtures('session')
def test_delete_all(session: Session) -> None:
    """Test delete all.

    :param session: sql alchemy db session
    :type session: Session
    """

    todo_view = TodoView(session)
    todo_view.add_todo('hello')
    todo_view.add_todo('world')
    todo_view.delete_todo_all()

    todos: Iterable[Todo] = session.query(Todo).all()
    assert len(todos) == 0
