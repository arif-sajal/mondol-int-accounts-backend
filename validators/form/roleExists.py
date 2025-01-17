from fastapi import HTTPException, status

# Import helpers
from helpers.database import db

# Import Models
from models.role import Role


async def role_exists(rid):
    role = await db.find_one(Role, Role.id == rid)
    if role is None:
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
    return role
