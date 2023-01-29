"""Manages cli argument parser for the application."""

import sys
from argparse import ArgumentParser
from dataclasses import dataclass

from todocli.base import get_session
from todocli.config import Config
from todocli.views import TodoView


@dataclass
class App:
    """Argument parser class. Create instance of this class to start the application.

    :param config: configurations
    :type config: Config
    """

    config: Config

    def __post_init__(self) -> None:
        """Create sqlalchemy db session."""
        self.todo_view: TodoView = TodoView(get_session(self.config))
        self.commands: dict[str, str] = {
            "list": "list_todo",
            "add": "add_todo",
            "update": "update_todo",
            "check": "check_todo",
            "uncheck": "uncheck_todo",
            "delete": "delete_todo",
        }

    def run(self) -> None:
        """Entry point for the argument parser class."""
        # main argument parser
        parser = ArgumentParser(
            description="todo-cli, a simple cli todo utility.",
            usage="python todo.py [-h] <command> [<args>]",
        )
        # list of possible commands
        parser.add_argument(
            "command",
            type=str,
            choices=["list", "add", "update", "check", "uncheck", "delete"],
        )
        # check first positional argument
        args = parser.parse_args(sys.argv[1:2])
        # call corresponding instance method if available
        getattr(self, self.commands[args.command])()

    def list_todo(self) -> None:
        """Argument parser and action for listing todo items."""
        parser = ArgumentParser(
            description="List todo items.", usage="python todo.py list [-h] [uid ...]"
        )
        parser.add_argument("uid", nargs="*", type=int, default=[], help="list by uid")
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        if args.uid:
            if len(args.uid) == 1:  # one item
                self.todo_view.list_todo(args.uid[0])
            else:  # main items
                self.todo_view.list_todo(args.uid)
        else:  # all items
            self.todo_view.list_todo()

    def add_todo(self) -> None:
        """Argument parser and action for adding todo items."""
        parser = ArgumentParser(
            description="Add todo item.",
            usage="python todo.py add [-h] title [title ...]",
        )
        parser.add_argument("title", nargs="+", type=str, help="todo title")
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        self.todo_view.add_todo(" ".join(args.title))

    def update_todo(self) -> None:
        """Argument parser and action for updating todo items."""
        parser = ArgumentParser(
            description="Update todo item.",
            usage="python todo.py update [-h] uid title [title ...]",
        )
        parser.add_argument("uid", type=int, help="update by uid")
        parser.add_argument("title", nargs="+", type=str, help="update title")
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        self.todo_view.update_todo(index=args.uid, title=" ".join(args.title))

    def _check_uncheck_helper(self, msg: str, check: bool) -> None:
        """Conditional action for marking checking todos."""
        usage = (
            f'python todo.py {msg.replace("-", "").lower()[:-1]} ' "[-h] [-a] [uid ...]"
        )
        parser = ArgumentParser(description=f"{msg} todo item.", usage=usage)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "uid", nargs="*", type=int, default=[], help=f"{msg.lower()} by uid"
        )
        group.add_argument(
            "-a", "--all", action="store_true", help=f"{msg.lower()} all"
        )
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        if args.uid:
            if len(args.uid) == 1:  # one item
                self.todo_view.update_todo(index=args.uid[0], check=check)
            else:  # many items
                self.todo_view.update_todo_check_many(indexes=args.uid, check=check)
        elif args.all:  # all items
            self.todo_view.update_todo_all(check)

    def check_todo(self) -> None:
        """Argument parser and action for checking todo items."""
        self._check_uncheck_helper("Checks", True)

    def uncheck_todo(self) -> None:
        """Argument parser and action for un-checking todo items."""
        self._check_uncheck_helper("Un-checks", False)

    def delete_todo(self) -> None:
        """Argument parser and action for deleting todo items."""
        parser = ArgumentParser(
            description="Delete todo item.",
            usage="python todo.py delete [-h] [-a] [uid ...]",
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("uid", nargs="*", type=int, default=[], help="delete by uid")
        group.add_argument("-a", "--all", action="store_true", help="delete all")
        # check positional argument from 2nd onwards
        args = parser.parse_args(sys.argv[2:])
        if args.uid:
            if len(args.uid) == 1:  # one item
                self.todo_view.delete_todo(args.uid[0])
            else:  # many items
                self.todo_view.delete_todo(args.uid)
        elif args.all:  # all items
            self.todo_view.delete_todo_all()
