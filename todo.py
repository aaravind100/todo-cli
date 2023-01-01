"""Main file for the todo cli application."""
from todocli import App


def main() -> None:
    """Entry point for the todo cli application."""
    app = App()
    app.run()


if __name__ == '__main__':
    main()
