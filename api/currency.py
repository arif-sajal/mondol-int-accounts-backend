from fastapi import APIRouter, Response, status, Depends
from odmantic.bson import ObjectId
from typing import List
from settings import settings

# Import Models
from models.currency import Currency

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.options import make as make_options
from helpers.auth import Auth

# Import Forms
from models.forms.currency import CreateCurrencyForm, UpdateCurrencyForm

# Import Responses
from models.response.currency import \
    CurrenciesPaginatedResults, \
    CurrencyResponse
from models.response.common import ErrorResponse, NotFound

# Import Utils
import datetime


api = APIRouter(
    prefix='/v1/currency',
    tags=["Currencies"],
    dependencies=[Depends(Auth().wrapper)]
)


@api.post(
    '/get-paginated',
    description='Get currencies with or without advanced filters.',
    responses={
        200: {'model': CurrenciesPaginatedResults}
    }
)
async def get_paginated_currencies(pagination: PaginationParameters):
    results = await prepare_result(Currency, pagination)
    return results


@api.get(
    '/get-as-options',
    description='Get currencies with filters as options.',
    responses={
        200: {'model': List[Currency]}
    }
)
async def get_currency_options(query: str = ''):
    results = await make_options(Currency, ['name', 'code'], query)
    return results


@api.get(
    '/get/{cid}',
    description='Get Single currency.',
    responses={
        200: {'model': Currency},
        404: {'model': NotFound}
    }
)
async def get_single_currency(cid: ObjectId, response: Response):
    currency = await db.find_one(Currency, Currency.id == cid)
    if currency is not None:
        return currency

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'currency'],
        msg='Country Not Found'
    )


@api.get(
    '/get-default',
    description='Get Default currency.',
    responses={
        200: {'model': Currency},
        404: {'model': NotFound}
    }
)
async def get_deFault_currency(response: Response):
    currency = await db.find_one(Currency, Currency.code == settings.LOCAL_CURRENCY)
    if currency is not None:
        return currency

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'default', 'currency'],
        msg='Currency Not Found'
    )


@api.post(
    '/create',
    description='Create new currency.',
    responses={
        200: {'model': CurrencyResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_currency(cur: CreateCurrencyForm, response: Response):
    currency = Currency(
        name=cur.name,
        code=cur.code,
        symbol=cur.symbol,
        rate=cur.rate
    )

    try:
        await db.save(currency)
        return CurrencyResponse(
            loc=['create', 'currency', 'success'],
            msg='Currency created successfully.',
            data=currency
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'currency', 'error'],
            msg='Can\'t create currency now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{cid}',
    description='Update currency.',
    responses={
        200: {'model': CurrencyResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def update_currency(cid: ObjectId, cou: UpdateCurrencyForm, response: Response):
    currency = await db.find_one(Currency, Currency.id == cid)

    if currency is not None:
        currency.name = cou.name
        currency.code = cou.code
        currency.symbol = cou.symbol
        currency.rate = cou.rate
        currency.updated_at = datetime.datetime.utcnow()

        try:
            await db.save(currency)
            return CurrencyResponse(
                loc=['update', 'currency', 'success'],
                msg='Currency updated successfully.',
                data=currency
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'currency', 'error'],
                msg='Can\'t update currency now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['currency', 'not', 'found'],
        msg='Currency not found with the provided ID.'
    )


@api.delete(
    '/delete/{cid}',
    description='Delete Country.',
    responses={
        200: {'model': CurrencyResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def delete_currency(cid: ObjectId, response: Response):
    currency = await db.find_one(Currency, Currency.id == cid)

    if currency is not None:
        try:
            if currency.code == settings.LOCAL_CURRENCY:
                response.status_code = status.HTTP_403_FORBIDDEN
                return ErrorResponse(
                    loc=['delete', 'currency', 'error'],
                    msg='Can\'t delete system default currency.'
                )

            await db.delete(currency)
            return CurrencyResponse(
                loc=['delete', 'currency', 'success'],
                msg='Currency deleted successfully.',
                data=currency
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'currency', 'error'],
                msg='Can\'t delete currency now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['currency', 'not', 'found'],
        msg='Currency not found with the provided ID.'
    )
