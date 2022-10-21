from pydantic import validator, EmailStr
from odmantic.bson import BaseBSONModel
from typing import List, Optional

# Import Validators
from validators.PhoneNumber import PhoneNumber
from validators.form.notEmpty import not_empty


class AdditionalInformation(BaseBSONModel):
    key: str
    value: str


class ContactForm(BaseBSONModel):
    name: str
    number: PhoneNumber
    email: Optional[EmailStr]
    af: Optional[List[AdditionalInformation]]

    # Validators
    _non_empty_fields = validator('name', allow_reuse=True)(not_empty)
