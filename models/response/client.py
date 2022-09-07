from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.client import ClientOut


class ClientsPaginatedResults(PaginationResult):
    data: Optional[List[ClientOut]]


class ClientResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[ClientOut], ClientOut]]
