from pymongo import TEXT
from pymongo.operations import IndexModel
from bunnet import Document
from pydantic import Field


class User(Document):
    id: int = Field(default_factory=int)
    moderator: bool = False
    administrator: bool = False


class Guild(Document):
    id: int = Field(default_factory=int)
    users: list[User] = []
