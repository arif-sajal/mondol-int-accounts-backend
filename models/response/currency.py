from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.currency import Currency


class CurrenciesPaginatedResults(PaginationResult):
    data: Optional[List[Currency]]


class CurrencyResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[Currency], Currency]]
