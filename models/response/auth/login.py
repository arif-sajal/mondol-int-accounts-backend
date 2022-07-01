from odmantic.bson import BaseBSONModel
from typing import Union

# Import Models
from models.admin import AdminOut
from models.role import Role
from models.client import Client


class LoginWithCredentialResponse(BaseBSONModel):
    access_token: str
    refresh_token: str


class LoginWithPhoneResponse(BaseBSONModel):
    access_token: str
    refresh_token: str


class RequestOtpForPhoneLoginResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str


class LoggedInUserResponse(BaseBSONModel):
    user: Union[AdminOut, Client]
    role: Union[Role, None]


class LoginErrorResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str
