"""Configurations."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import yaml

CONFIG_FILE = 'config.yaml'  # config file name
# file path from parent dir
CONFIG_FILE_PATH = Path(__file__).resolve().parent.parent.joinpath(CONFIG_FILE)

with open(CONFIG_FILE_PATH, 'r', encoding='utf8') as file:
    CONFIG = yaml.safe_load(file)


class Icons(Enum):
    """Emoji icons for todo status."""
    CHECK = CONFIG['icons']['check']
    UNCHECK = CONFIG['icons']['uncheck']


@dataclass
class Config:
    """Configurations.

    :param db_dialect: sql alchemy db dialect
    :type db_dialect: str
    """
    db_dialect: str = CONFIG['db_dialect']
