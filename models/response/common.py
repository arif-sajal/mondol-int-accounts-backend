from odmantic.bson import BaseBSONModel
from typing import List, Union


class ErrorResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str


class NotFound(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
