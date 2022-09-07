from fastapi import HTTPException, status

# Import helpers
from helpers.database import db

# Import Models
from models.account import Account


async def account_exists(aid, loc=None):
    account = await db.find_one(Account, Account.id == aid)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                dict(
                    loc=list(set(['body', 'account'] + loc)),
                    msg='not exists',
                    type='value_error.not.exists'
                )
            ]
        )
    return account
