from pydantic import validator, EmailStr
from odmantic.bson import BaseBSONModel, ObjectId

# Import Validators
from validators.PhoneNumber import PhoneNumber
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
    _match_confirm_password = validator('confirm_password', allow_reuse=True)(match_confirm_password)


class UpdateAdminForm(BaseBSONModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    role: ObjectId


class ChangeAdminPasswordForm(BaseBSONModel):
    password: str
    confirm_password: str

    # Validators
    _match_confirm_password = validator('confirm_password', allow_reuse=True)(match_confirm_password)
