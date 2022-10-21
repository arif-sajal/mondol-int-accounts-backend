from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.contact import Contact


class ContactsPaginatedResults(PaginationResult):
    data: Optional[List[Contact]]


class ContactResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[Contact], Contact]]
