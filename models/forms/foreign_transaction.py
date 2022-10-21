from pydantic import validator
from odmantic.bson import BaseBSONModel, ObjectId
from typing import Optional

# Import Models
from models import TransactionType

# Import Validators
from validators.form.notEmpty import not_empty


class ForeignTransactionForm(BaseBSONModel):
    from_currency: ObjectId
    rate: float
    amount: float
    type: TransactionType
    client: ObjectId
    ad_rate: float
    note: str
    remark: str
    created_at: Optional[str]

    # Validators
    _non_empty_fields = validator('type', 'client', allow_reuse=True)(not_empty)
