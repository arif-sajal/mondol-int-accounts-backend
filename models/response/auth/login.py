from odmantic.bson import BaseBSONModel
from typing import List, Union


class LoginWithCredentialResponse(BaseBSONModel):
    access_token: str
    refresh_token: str


class LoginWithPhoneResponse(BaseBSONModel):
    access_token: str
    refresh_token: str


class RequestOtpForPhoneLoginResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str


class LoginErrorResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str
