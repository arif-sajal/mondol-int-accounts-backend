from fastapi import APIRouter, Response, status
from odmantic.bson import ObjectId
from typing import List

# Import Models
from models.country import Country
from models.client import Client

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.options import make as make_options

# Import Forms
from models.forms.country import CountryForm

# Import Responses
from models.response.country import\
    CountriesPaginatedResults,\
    CountryResponse
from models.response.common import ErrorResponse, NotFound

api = APIRouter(
    prefix='/v1/country',
    tags=["Countries"]
)


@api.post(
    '/get-paginated',
    description='Get countries with or without advanced filters.',
    responses={
        200: {'model': CountriesPaginatedResults}
    }
)
async def get_paginated_countries(pagination: PaginationParameters):
    results = await prepare_result(Country, pagination)
    return results


@api.get(
    '/get-as-options',
    description='Get countries with filters as options.',
    responses={
        200: {'model': List[Country]}
    }
)
async def get_country_options(query: str = ''):
    results = await make_options(Country, ['name', 'code'], query)
    return results


@api.get(
    '/get/{cid}',
    description='Get Single country.',
    responses={
        200: {'model': Country},
        404: {'model': NotFound}
    }
)
async def get_single_country(cid: ObjectId, response: Response):
    country = await db.find_one(Country, Country.id == cid)
    if country is not None:
        return country

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'country'],
        msg='Country Not Found'
    )


@api.post(
    '/create',
    description='Create new country.',
    responses={
        200: {'model': CountryResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_country(cou: CountryForm, response: Response):
    country = Country(
        name=cou.name,
        code=cou.code
    )

    try:
        await db.save(country)
        return CountryResponse(
            loc=['create', 'country', 'success'],
            msg='Country created successfully.',
            data=country
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'country', 'error'],
            msg='Can\'t create country now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{cid}',
    description='Update country.',
    responses={
        200: {'model': CountryResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def update_country(cid: ObjectId, cou: CountryForm, response: Response):
    country = await db.find_one(Country, Country.id == cid)

    if country is not None:
        country.name = cou.name
        country.code = cou.code

        try:
            await db.save(country)
            return CountryResponse(
                loc=['update', 'country', 'success'],
                msg='Country updated successfully.',
                data=country
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'country', 'error'],
                msg='Can\'t update country now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['country', 'not', 'found'],
        msg='Country not found with the provided ID.'
    )


@api.delete(
    '/delete/{cid}',
    description='Delete Country.',
    responses={
        200: {'model': CountryResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def delete_country(cid: ObjectId, response: Response):
    country = await db.find_one(Country, Country.id == cid)

    if country is not None:
        clients = len(await db.find(Client, Client.country == country.id))
        if clients > 0:
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'country', 'error'],
                msg=f'Can\'t delete this country, {clients} Clients exists from this country.'
            )

        try:
            await db.delete(country)
            return CountryResponse(
                loc=['delete', 'country', 'success'],
                msg='Country deleted successfully.',
                data=country
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'country', 'error'],
                msg='Can\'t delete country now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['country', 'not', 'found'],
        msg='Country not found with the provided ID.'
    )
