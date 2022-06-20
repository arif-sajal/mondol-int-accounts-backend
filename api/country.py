from fastapi import APIRouter, Response, status

# Import Models
from models.country import Country

# Import Helpers
from helpers.pagination import prepare_result, PaginationParameters

# Import Responses
from models.response.country import CountriesPaginatedResults

api = APIRouter(
    prefix='/v1/country',
    tags=["Countries"],
)


@api.post(
    '/get',
    description='Get countries with or without filters.',
    responses={
        200: {'model': CountriesPaginatedResults}
    }
)
async def get(pagination: PaginationParameters):
    results = await prepare_result(Country, pagination)
    return results
