from pydantic import EmailStr
from odmantic import Model, EmbeddedModel, Field
from typing import List, Optional

# Import Validator
from validators.PhoneNumber import PhoneNumber

# Import Utils
import datetime


class AdditionalInformation(EmbeddedModel):
    key: str
    value: str


class Contact(Model):
    name: str
    number: PhoneNumber
    email: Optional[EmailStr]
    af: List[AdditionalInformation]

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
