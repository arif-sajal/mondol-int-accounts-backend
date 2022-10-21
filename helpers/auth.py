# Import FastApi
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from typing import Union
from odmantic import ObjectId

# Import Helpers
from helpers.database import db

# Import Models
from models.admin import Admin
from models.client import Client

# Import settings
from settings import settings

# Import Utilities
from datetime import datetime, timedelta
import jwt


async def get_user(user_id, user_type):
    user = None
    if user_type == 'admin':
        user = await db.find_one(Admin, Admin.id == user_id)
    if user_type == 'client':
        user = await db.find_one(Client, Client.id == user_id)
    return user


class Auth:

    def __init__(self):
        self.password_context = CryptContext(schemes=['bcrypt'])
        self.secret = settings.APP_SECRET
        self.algorithm = settings.APP_ALGORITHM

    def encode_password(self, password):
        return self.password_context.hash(password)

    def verify_password(self, plain_password, hash_password):
        return self.password_context.verify(plain_password, hash_password)

    def encode_token(self, user: Union[Admin, Client]):
        payload = {
            "user": {
                "id": str(user.id),
                "role": isinstance(user, Admin) and str(user.role.id) or None,
                "type": isinstance(user, Admin) and 'admin' or 'client'
            },
            "expiry": str(datetime.utcnow() + timedelta(minutes=30))
        }

        e_token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return e_token

    def decode_token(self, token: str):
        try:
            d_token = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return d_token if datetime.strptime(d_token['expiry'],
                                                '%Y-%m-%d %H:%M:%S.%f') >= datetime.utcnow() else None
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Auth Token Expired.')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid Auth Token Supplied.')

    def encode_refresh_token(self, user: Union[Admin, Client]):
        payload = {
            "user": {
                "id": str(user.id),
                "role": isinstance(user, Admin) and str(user.role.id) or None,
                "type": isinstance(user, Admin) and 'admin' or 'client'
            },
            "expiry": str(datetime.utcnow() + timedelta(days=365))
        }

        e_token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return e_token

    def decode_refresh_token(self, token: str):
        try:
            d_token = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return d_token if datetime.strptime(d_token['expiry'], '%Y-%m-%d %H:%M:%S.%f') >= datetime.utcnow() else None
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh Token Expired.')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid Refresh Token Supplied.')

    async def wrapper(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        token = self.decode_token(auth.credentials)
        if token and 'user' in token:
            user = await get_user(ObjectId(token['user']['id']), token['user']['type'])
            if user is not None:
                return token
        raise HTTPException(status_code=401, detail='Invalid Access Token Supplied.')
