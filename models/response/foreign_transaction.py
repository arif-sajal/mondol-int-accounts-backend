from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.foreign_transaction import ForeignTransaction


class ForeignTransactionPaginatedResults(PaginationResult):
    data: Optional[List[ForeignTransaction]]


class ForeignTransactionResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[ForeignTransaction], ForeignTransaction]]
