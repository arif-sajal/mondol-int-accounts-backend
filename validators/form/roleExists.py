# Import helpers
from helpers.database import db

# Import Models
from models.role import Role


async def role_exists(rid):
    role = await db.find_one(Role, Role.id == rid)
    if role is not None:
        return role
    return False
