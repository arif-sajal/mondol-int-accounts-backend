from odmantic import Model, Field, ObjectId, Reference
from enum import Enum

# Import Models
from models.client import ClientOut
from models.currency import Currency
from models import TransactionType

# Import Helpers
from helpers.database import db

# Import Utils
import datetime


class TranBound(str, Enum):
    FOREIGN = 'FOREIGN'
    LOCAL = 'LOCAL'


class Transaction(Model):
    tran_id: ObjectId
    tran_bound: TranBound
    tran_type: TransactionType
    client: ClientOut = Reference()
    currency: Currency = Reference()
    amount: float

    ad_currency: Currency = Reference()
    ad_rate: float
    ad_amount: float

    client_balance: float
    client_ad_balance: float

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    async def previous_balance_state(self):
        if self.tran_type == TransactionType.PAID:
            self.client.balance -= self.amount
            self.client.ad_balance -= self.ad_amount

        if self.tran_type == TransactionType.RECEIVED:
            self.client.balance += self.amount
            self.client.ad_balance += self.ad_amount

        try:
            await db.save(self.client)
            return True
        except():
            return False

    async def next_balance_state(self):
        if self.tran_type == TransactionType.PAID:
            self.client.balance += self.amount
            self.client.ad_balance += self.ad_amount

        if self.tran_type == TransactionType.RECEIVED:
            self.client.balance -= self.amount
            self.client.ad_balance -= self.ad_amount

        try:
            await db.save(self.client)
            return True
        except():
            return False

    class Config:
        title = 'Main Transaction Model'
        collection = "transactions"
