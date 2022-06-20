from typing import Optional, List

# Import Helpers
from helpers.pagination import PaginationResult

# Import Models
from models.country import Country


class CountriesPaginatedResults(PaginationResult):
    data: Optional[List[Country]]
