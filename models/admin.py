from odmantic import Model, Reference, Field
from pydantic import EmailStr, FilePath
from typing import Optional

# Import Models
from models.role import Role

# Import Utility Validators
from validators.PhoneNumber import PhoneNumber


class Admin(Model):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    password: str
    status: bool = Field(default=False)
    avatar: Optional[FilePath]
    role: Role = Reference()

    class Config:
        collection = "admins"
