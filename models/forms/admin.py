from pydantic import validator, EmailStr
from odmantic.bson import BaseBSONModel, ObjectId

# Import Validators
from validators.PhoneNumber import PhoneNumber
from validators.form.matchConfirmPassword import match_confirm_password
from validators.form.roleExists import role_exists

# Import Models
from models.role import Role

# Import Helpers
from helpers.database import db


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
    # _confirm_role_existence = validator('role', allow_reuse=True)(role_exists)


class UpdateAdminForm(BaseBSONModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    username: str
    role: ObjectId

    # Validators
    _confirm_role_existence = validator('role', allow_reuse=True)(role_exists)


class ChangeAdminPasswordForm(BaseBSONModel):
    password: str
    confirm_password: str

    # Validators
    _match_confirm_password = validator('confirm_password', allow_reuse=True)(match_confirm_password)
