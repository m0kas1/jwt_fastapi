from beanie import Document, Link
from .User import User
from pymongo import IndexModel, ASCENDING

class Token(Document):
    id_user: Link[User]
    refresh_token: str

    class Settings:
        name = "refresh_token"
        indexes = [
            IndexModel([("refresh_token", ASCENDING)], unique=True)
        ]