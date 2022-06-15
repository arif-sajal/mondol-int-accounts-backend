from odmantic import Model, Reference, Field
from pydantic import EmailStr, FilePath
from typing import Optional

# Import Models
from models.country import Country

# Import Utility Validators
from validators.PhoneNumber import PhoneNumber


class Client(Model):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    password: str
    status: bool = Field(default=False)
    avatar: Optional[FilePath]
    country: Country = Reference()

    class Config:
        collection = "clients"
