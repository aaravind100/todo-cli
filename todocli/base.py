"""Base for database connections."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from todocli.config import Config

Base = declarative_base()


def get_session(config: Config) -> Session:
    """Create sqlalchemy db session.

    :param config: configurations
    :type config: Config
    :return: sql alchemy db session
    :rtype: Session
    """
    engine = create_engine(config.db_dialect, echo=False)
    Base.metadata.create_all(engine)  # create tables for models
    session = sessionmaker(bind=engine)
    return session()
