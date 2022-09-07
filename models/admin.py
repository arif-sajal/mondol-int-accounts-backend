from odmantic import Model, Reference, Field
from pydantic import EmailStr, FilePath
from typing import Optional

# Import Models
from models.role import Role, RoleOut
from models.auth import PhoneLogin, ResetPassword

# Import Utility Validators
from validators.PhoneNumber import PhoneNumber

# Import Utils
import datetime


class Admin(Model):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    password: str
    phone_login: Optional[PhoneLogin]
    reset_password: Optional[ResetPassword]
    status: bool = Field(default=False)
    avatar: Optional[FilePath]
    role: Role = Reference()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main admin model for internal use.'
        collection = "admins"


class AdminOut(Model):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    status: bool = Field(default=False)
    avatar: Optional[FilePath]
    role: RoleOut = Reference()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Admin model for external use.'
        collection = "admins"
