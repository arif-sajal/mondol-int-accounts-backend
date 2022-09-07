from odmantic import Model, Reference, Field
from pydantic import EmailStr, FilePath
from typing import Optional

# Import Models
from .country import Country
from .auth import PhoneLogin, ResetPassword

# Import Utility Validators
from validators.PhoneNumber import PhoneNumber

# Import Utils
import datetime


class Client(Model):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    password: str
    phone_login: Optional[PhoneLogin]
    reset_password: Optional[ResetPassword]
    status: bool = Field(default=False)
    avatar: Optional[FilePath]
    country: Country = Reference()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        collection = "clients"


class ClientOut(Model):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    status: bool = Field(default=False)
    avatar: Optional[FilePath]
    country: Country = Reference()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        collection = "clients"
