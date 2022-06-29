from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.admin import AdminOut


class AdminsPaginatedResults(PaginationResult):
    data: Optional[List[AdminOut]]


class AdminResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[AdminOut], AdminOut]]
