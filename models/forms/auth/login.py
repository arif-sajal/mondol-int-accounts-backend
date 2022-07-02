from pydantic import validator
from odmantic.bson import BaseBSONModel

# Import Validators
from validators.PhoneNumber import PhoneNumber
from validators.form.notEmpty import not_empty


class LoginWithCredentialForm(BaseBSONModel):
    username: str
    password: str

    # Validators
    _not_empty_username = validator('username', allow_reuse=True)(not_empty)
    _not_empty_password = validator('password', allow_reuse=True)(not_empty)


class RequestOtpForPhoneLoginForm(BaseBSONModel):
    phone: PhoneNumber

    # Validators
    _not_empty_phone = validator('phone', allow_reuse=True)(not_empty)


class LoginWithPhoneForm(BaseBSONModel):
    phone: PhoneNumber
    code: str

    # Validators
    _not_empty_phone = validator('phone', allow_reuse=True)(not_empty)
    _not_empty_code = validator('code', allow_reuse=True)(not_empty)


class RefreshTokenForm(BaseBSONModel):
    refresh_token: str

    # Validators
    _not_empty_phone = validator('refresh_token', allow_reuse=True)(not_empty)
