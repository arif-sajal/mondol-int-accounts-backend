from fastapi import APIRouter

# Import Helpers
from helpers.auth import Auth
from helpers.database import db

api = APIRouter(
    prefix='/v1/auth',
    tags=["Authentication"]
)


@api.post('/login-with-credential', description='Login with username and password')
async def login_with_credential():
    admin = await db.find_one('')
