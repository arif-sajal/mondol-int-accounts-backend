from odmantic import Model, Field, Reference

# Import Models
from .client import Client
from .currency import Currency

# Import Utils
import datetime


class Balance(Model):
    client: Client = Reference()
    currency: Currency = Reference()
    balance: float = Field(default=0.00)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main Balance Model for internal use.'
        collection = "balances"
