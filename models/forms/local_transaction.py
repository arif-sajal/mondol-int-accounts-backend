from pydantic import validator
from odmantic.bson import BaseBSONModel, ObjectId
from typing import Optional

# Import Models
from models import TransactionType

# Import Validators
from validators.form.notEmpty import not_empty


class LocalTransactionForm(BaseBSONModel):
    client: ObjectId
    amount: float
    type: TransactionType
    account: ObjectId
    note: Optional[str]
    ad_rate: Optional[float]
    ad_amount: Optional[float]
    remark: Optional[str]
    created_at: Optional[str]

    # Validators
    _non_empty_fields = validator('type', 'account', 'client', 'amount', allow_reuse=True)(not_empty)
