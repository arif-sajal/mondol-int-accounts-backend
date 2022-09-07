from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.account import Account


class AccountsPaginatedResults(PaginationResult):
    data: Optional[List[Account]]


class AccountResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[Account], Account]]
