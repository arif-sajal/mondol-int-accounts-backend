from pydantic import validator, EmailStr
from odmantic.bson import BaseBSONModel, ObjectId

# Import Validators
from validators.PhoneNumber import PhoneNumber
from validators.form.notEmpty import not_empty
from validators.form.matchConfirmPassword import match_confirm_password


class CreateAdminForm(BaseBSONModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    password: str
    confirm_password: str
    role: ObjectId

    # Validators
    _non_empty_fields = validator('name', 'email', 'phone', 'username', 'password', 'confirm_password', 'role', allow_reuse=True)(not_empty)
    _match_confirm_password = validator('confirm_password', allow_reuse=True)(match_confirm_password)


class UpdateAdminForm(BaseBSONModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    role: ObjectId

    # Validators
    _non_empty_fields = validator('name', 'email', 'phone', 'username', 'role', allow_reuse=True)(not_empty)


class ChangeAdminPasswordForm(BaseBSONModel):
    password: str
    confirm_password: str

    # Validators
    _non_empty_fields = validator('password', 'confirm_password', allow_reuse=True)(not_empty)
    _match_confirm_password = validator('confirm_password', allow_reuse=True)(match_confirm_password)
