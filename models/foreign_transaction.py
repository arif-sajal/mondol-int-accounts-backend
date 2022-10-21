from odmantic import Model, Field, Reference
from typing import Optional

# Import Models
from . import TransactionType
from .currency import Currency
from .client import ClientOut
from .transaction import Transaction, TranBound

# Import Helpers
from helpers.database import db

# Import Utils
import datetime


class ForeignTransaction(Model):
    from_currency: Currency = Reference()
    to_currency: Currency = Reference()

    rate: float
    amount: float
    cv_amount: float

    type: TransactionType

    client: ClientOut = Reference()
    ad_currency: Currency = Reference()
    ad_rate: float
    ad_cv_amount: float

    note: Optional[str]
    remark: Optional[str]

    client_balance: float
    client_ad_balance: float

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    async def create_ledger(self):
        client_balance = 0
        client_ad_balance = 0

        if self.type == TransactionType.PAID:
            client_balance = self.client.balance + self.cv_amount
            client_ad_balance = self.client.ad_balance + self.ad_cv_amount

        if self.type == TransactionType.RECEIVED:
            client_balance = self.client.balance - self.cv_amount
            client_ad_balance = self.client.ad_balance - self.ad_cv_amount

        transaction = Transaction(
            tran_id=self.id,
            tran_bound=TranBound.FOREIGN,
            tran_type=self.type,
            client=self.client,
            currency=self.to_currency,
            amount=self.cv_amount,
            ad_currency=self.ad_currency,
            ad_rate=self.ad_rate,
            ad_amount=self.ad_cv_amount,
            client_balance=client_balance,
            client_ad_balance=client_ad_balance,
            created_at=self.created_at
        )
        try:
            await db.save(transaction)
            await transaction.next_balance_state()
            return True
        except():
            return False

    async def update_ledger(self):
        transaction = await db.find_one(Transaction, Transaction.tran_id == self.id,
                                        Transaction.tran_bound == TranBound.FOREIGN)
        await transaction.previous_balance_state()
        transaction.tran_type = self.type
        transaction.client = self.client
        transaction.amount = self.amount
        transaction.currency = self.ad_currency
        transaction.rate = self.ad_rate
        transaction.ad_amount = self.ad_cv_amount

        diff = transaction.amount - self.cv_amount

        if self.type == TransactionType.PAID:
            transaction.client_balance += diff
            transaction.client_ad_balance += diff

        if self.type == TransactionType.RECEIVED:
            transaction.client_balance -= diff
            transaction.client_balance -= diff

        try:
            await transaction.next_balance_state()
            await db.save(transaction)
            return True
        except():
            return False

    async def delete_ledger(self):
        transaction = await db.find_one(Transaction, Transaction.tran_id == self.id,
                                        Transaction.tran_bound == TranBound.FOREIGN)
        try:
            await transaction.previous_balance_state()
            await db.delete(transaction)
            return True
        except():
            return False

    class Config:
        title = 'Main Foreign Transaction Model'
        collection = "foreign_transactions"
