from odmantic.bson import BaseBSONModel
from typing import Union


class ResetPasswordErrorResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str


class RequestResetPasswordOtpResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str


class VerifyResetPasswordOtpResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str


class ResetPasswordResponse(BaseBSONModel):
    loc: list[Union[str, int]]
    msg: str
