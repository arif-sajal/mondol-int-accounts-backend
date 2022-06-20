# Import Models
from models.admin import Admin
from models.client import Client

# Import Helpers
from helpers.database import db


class User:

    def __init__(self, query=None):
        self.admin = Admin
        self.client = Client
        self.db = db
        self.query = query

    async def get_admins(self):
        return await self.db.find(self.admin, self.query)

    async def get_admin(self):
        return await self.db.find_one(self.admin, self.query)

    async def get_admin_by_username(self):
        return await self.db.find_one(self.admin, self.admin.username == self.query)

    async def get_admin_by_email(self):
        return await self.db.find_one(self.admin, self.admin.email == self.query)

    async def get_admin_by_phone(self):
        return await self.db.find_one(self.admin, self.admin.phone == self.query)

    async def get_clients(self):
        return await self.db.find(self.client, self.query)

    async def get_client(self):
        return await self.db.find_one(self.client, self.query)

    async def get_client_by_username(self):
        return await self.db.find_one(self.client, self.admin.username == self.query)

    async def get_client_by_email(self):
        return await self.db.find_one(self.client, self.admin.email == self.query)

    async def get_client_by_phone(self):
        return await self.db.find_one(self.client, self.admin.phone == self.query)

    def query(self, query):
        self.query = query
        return self
