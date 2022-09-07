from fastapi import HTTPException, status
from odmantic.bson import ObjectId
from typing import List

# Import helpers
from helpers.database import db

# Import Models
from models.currency import Currency


async def currency_exists(cid: ObjectId, loc=None):
    if loc is None:
        loc = []
    loc = ['body'] + loc + ['currency']

    currency = await db.find_one(Currency, Currency.id == cid)
    if currency is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                dict(
                    loc=loc,
                    msg='not exists',
                    type='value_error.not.exists'
                )
            ]
        )

    return currency


async def currencies_exists(cids: List[ObjectId], loc=None):
    if loc is None:
        loc = []
    loc = ['body'] + loc

    errors = list()
    if isinstance(cids, List):
        for i, cid in enumerate(cids):
            country = await db.find_one(Currency, Currency.id == cid)
            if country is None:
                errors.append(
                    dict(
                        loc=loc + [i, 'currency'],
                        msg='not exists',
                        type='value_error.not.exists'
                    )
                )

    if len(errors) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors
        )
