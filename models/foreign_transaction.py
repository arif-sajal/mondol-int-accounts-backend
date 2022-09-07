from odmantic import Model, Field, Reference
from odmantic.bson import ObjectId
from typing import Optional

# Import Models
from . import TransactionType, TransactionReferenceType
from .currency import Currency

# Import Utils
import datetime


class ForeignTransaction(Model):
    from_currency: Currency = Reference()
    to_currency: Currency = Reference()

    rate: float
    amount: float
    cv_amount: float

    type: TransactionType

    reference_type: TransactionReferenceType
    reference: ObjectId

    note: Optional[str]
    remark: Optional[str]

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main Foreign Transaction Model'
        collection = "foreign_transactions"
