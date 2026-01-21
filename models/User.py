from beanie import Document
from pydantic import BaseModel, Field
from pymongo import IndexModel, ASCENDING

class Roli_na_ruke(BaseModel):
    name_role: str

class User(Document):
    username: str = Field(min_length=4, max_length=20)
    password: str
    roles: list[Roli_na_ruke] = [Roli_na_ruke(name_role="USER")]

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("username", ASCENDING)], unique=True)
        ]