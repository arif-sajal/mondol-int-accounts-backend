from odmantic.bson import BaseBSONModel
from typing import Optional, List, Union

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.country import Country


class CountriesPaginatedResults(PaginationResult):
    data: Optional[List[Country]]


class CountryResponse(BaseBSONModel):
    loc: List[Union[str, int]]
    msg: str
    data: Optional[Union[List[Country], Country]]

