from odmantic.bson import BaseBSONModel

# Import Validators
from validators.PhoneNumber import PhoneNumber


class LoginWithCredentialForm(BaseBSONModel):
    username: str
    password: str


class RequestOtpForPhoneLoginForm(BaseBSONModel):
    phone: PhoneNumber


class LoginWithPhoneForm(BaseBSONModel):
    phone: PhoneNumber
    code: str


class RefreshTokenForm(BaseBSONModel):
    refresh_token: str
