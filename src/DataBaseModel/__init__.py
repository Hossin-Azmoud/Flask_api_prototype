from dataclasses import dataclass

from .Models import (
	UserModel, 
	ConstructModel, 
	PostModel,
	response
)

from .Database import DB, constructDB
from os import environ


DB_PATH = environ["db"]
