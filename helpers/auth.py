# Import FastApi
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from typing import Union

# Import Models
from models.admin import Admin
from models.client import Client

# Import settings
from settings import settings

# Import Utilities
from datetime import datetime, timedelta
import jwt


class Auth:

    security = HTTPBearer()

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
            "user": user.id,
            "type": isinstance(user, Admin) and 'admin' or 'client',
            "expiry": datetime.utcnow() + timedelta(days=7)
        }

        e_token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return e_token

    def decode_token(self, token: str):
        try:
            d_token = jwt.decode(token, self.secret, algorithm=self.algorithm)
            return d_token if d_token['expiry'] >= datetime.utcnow() else None
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Auth Token Expired.')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid Auth Token Supplied.')

    def wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
