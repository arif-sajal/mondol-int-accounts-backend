from odmantic import Model, Field
from odmantic.bson import ObjectId
from typing import Optional

# Import Models
from . import TransactionType, TransactionReferenceType

# Import Utils
import datetime


class LocalTransaction(Model):
    amount: float

    type: TransactionType

    reference_type: TransactionReferenceType
    reference: ObjectId

    note: Optional[str]
    remark: Optional[str]

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main Local Transaction Model for internal use'
        collection = "local_transactions"
