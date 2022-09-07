# Import Models
from models.balance import Balance as Bal
from models.client import Client
from models.currency import Currency

# Import Helpers
from helpers.database import db

# Import Utils
from bson import ObjectId


class Balance:

    def __init__(self, client=None, balance=None, currency=None):
        self.client = client
        self.balance = balance
        self.currency = currency

    async def get(self):
        balance = None
        if self.client is not None:
            client_id = None
            if isinstance(self.client, Client):
                client_id = self.client.id
            elif ObjectId.is_valid(self.client):
                client_id = self.client

            currency_id = None
            if isinstance(self.currency, Currency):
                currency_id = self.currency.id
            elif ObjectId.is_valid(self.currency):
                currency_id = self.currency

            if client_id is not None:
                if currency_id is None:
                    balance = await db.find(Bal, Bal.client == client_id)
                else:
                    balance = await db.find_one(Bal, Bal.client == client_id, Bal.currency == currency_id)
        elif self.balance is not None:
            balance = await db.find_one(Bal, Bal.id == self.balance)

        return balance

    async def increment(self, amount):
        balance = await self.get()
        balance.balance = balance.balance + float(amount)
        return await db.save(balance)

    async def decrement(self, amount):
        balance = await self.get()
        balance.balance = balance.balance - float(amount)
        return await db.save(balance)
