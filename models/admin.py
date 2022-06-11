from odmantic import Model
from pydantic import EmailStr, FilePath
from typing import Optional


class Admin(Model):
    name: str
    email: EmailStr
    username: str
    password: str
    avatar: Optional[FilePath]

    class Config:
        collection = "admins"
