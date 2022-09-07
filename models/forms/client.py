from pydantic import validator, EmailStr
from odmantic.bson import BaseBSONModel, ObjectId

# Import Validators
from validators.PhoneNumber import PhoneNumber
from validators.form.notEmpty import not_empty
from validators.form.matchConfirmPassword import match_confirm_password


class CreateClientForm(BaseBSONModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    password: str
    confirm_password: str
    country: ObjectId

    # Validators
    _non_empty_fields = validator('name', 'email', 'phone', 'username', 'password', 'confirm_password', 'country', allow_reuse=True)(not_empty)
    _match_confirm_password = validator('confirm_password', allow_reuse=True)(match_confirm_password)


class UpdateClientForm(BaseBSONModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    country: ObjectId

    # Validators
    _non_empty_fields = validator('name', 'email', 'phone', 'username', 'country', allow_reuse=True)(not_empty)


class ChangeClientPasswordForm(BaseBSONModel):
    password: str
    confirm_password: str

    # Validators
    _non_empty_fields = validator('password', 'confirm_password', allow_reuse=True)(not_empty)
    _match_confirm_password = validator('confirm_password', allow_reuse=True)(match_confirm_password)
