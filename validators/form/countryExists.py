from fastapi import HTTPException, status

# Import helpers
from helpers.database import db

# Import Models
from models.country import Country


async def country_exists(cid):
    country = await db.find_one(Country, Country.id == cid)
    if country is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                dict(
                    loc=['body', 'country'],
                    msg='not exists',
                    type='value_error.not.exists'
                )
            ]
        )
    return country
