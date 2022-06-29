from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.role import Role


class RolesPaginatedResults(PaginationResult):
    data: Optional[List[Role]]


class RoleResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[Role], Role]]
