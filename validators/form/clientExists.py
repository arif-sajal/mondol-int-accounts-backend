from fastapi import HTTPException, status

# Import helpers
from helpers.database import db

# Import Models
from models.client import Client


async def client_exists(cid, loc=None):
    client = await db.find_one(Client, Client.id == cid)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                dict(
                    loc=list(set(['body', 'client'] + loc)),
                    msg='not exists',
                    type='value_error.not.exists'
                )
            ]
        )
    return client
