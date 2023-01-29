"""Main file for the todo cli application."""
from todocli import App, Config


def main() -> None:
    """Entry point for the todo cli application."""
    app = App(Config())
    app.run()


if __name__ == "__main__":
    main()
