from odmantic import Model, Field, Reference
from typing import Optional

# Import Helpers
from helpers.database import db

# Import Models
from . import TransactionType
from .account import Account
from .client import ClientOut
from .transaction import Transaction, TranBound, Currency

# Import Utils
from settings import settings
import datetime


class LocalTransaction(Model):
    amount: float

    type: TransactionType

    account: Account = Reference()
    client: ClientOut = Reference()

    ad_currency: Currency = Reference()
    ad_rate: float
    ad_amount: float

    note: Optional[str]
    remark: Optional[str]

    client_balance: float
    client_ad_balance: float

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    async def account_prev_state(self):
        if self.type == TransactionType.PAID:
            self.account.balance += self.amount

        if self.type == TransactionType.RECEIVED:
            self.account.balance -= self.amount

        try:
            await db.save(self.account)
            return True
        except():
            return False

    async def account_next_state(self):
        if self.type == TransactionType.PAID:
            self.account.balance -= self.amount

        if self.type == TransactionType.RECEIVED:
            self.account.balance += self.amount

        try:
            await db.save(self.account)
            return True
        except():
            return False

    async def create_ledger(self):
        currency = await db.find_one(Currency, Currency.code == settings.LOCAL_CURRENCY)

        client_balance = 0
        client_ad_balance = 0

        if self.type == TransactionType.PAID:
            client_balance = self.client.balance + self.amount
            client_ad_balance = self.client.ad_balance + self.ad_amount

        if self.type == TransactionType.RECEIVED:
            client_balance = self.client.balance - self.amount
            client_ad_balance = self.client.ad_balance - self.ad_amount

        transaction = Transaction(
            tran_id=self.id,
            tran_bound=TranBound.LOCAL,
            tran_type=self.type,
            client=self.client,
            currency=currency,
            amount=self.amount,
            ad_currency=self.client.currency,
            ad_rate=self.ad_rate,
            ad_amount=self.ad_amount,
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
                                        Transaction.tran_bound == TranBound.LOCAL)
        await transaction.previous_balance_state()
        transaction.tran_type = self.type
        transaction.client = self.client
        transaction.amount = self.amount
        transaction.currency = self.client.currency
        transaction.ad_rate = self.ad_rate
        transaction.ad_amount = self.ad_amount

        diff = transaction.amount - self.amount

        if self.type == TransactionType.PAID:
            transaction.client_balance += diff
            transaction.client_ad_balance += diff

        if self.type == TransactionType.RECEIVED:
            transaction.client_balance -= diff
            transaction.client_balance -= diff

        try:
            await db.save(transaction)
            await transaction.next_balance_state()
            return True
        except():
            return False

    async def delete_ledger(self):
        transaction = await db.find_one(Transaction, Transaction.tran_id == self.id,
                                        Transaction.tran_bound == TranBound.LOCAL)
        try:
            await transaction.previous_balance_state()
            await db.delete(transaction)
            return True
        except():
            return False

    class Config:
        title = 'Main Local Transaction Model for internal use'
        collection = "local_transactions"
