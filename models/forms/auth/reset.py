from odmantic.bson import BaseBSONModel
from pydantic import EmailStr
from enum import Enum
from typing import Union

# Import Validators
from validators.PhoneNumber import PhoneNumber


class ResetRequestMethod(str, Enum):
    email = 'email'
    phone = 'phone'


class RequestResetPasswordOtpForm(BaseBSONModel):
    identity: Union[EmailStr, PhoneNumber]
    method: ResetRequestMethod


class VerifyResetPasswordOtpForm(BaseBSONModel):
    identity: Union[EmailStr, PhoneNumber]
    code: str


class ResetPasswordForm(BaseBSONModel):
    identity: Union[EmailStr, PhoneNumber]
    password: str
    confirm_password: str
