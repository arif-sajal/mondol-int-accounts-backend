from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.local_transaction import LocalTransaction


class LocalTransactionPaginatedResults(PaginationResult):
    data: Optional[List[LocalTransaction]]


class LocalTransactionResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[LocalTransaction], LocalTransaction]]
