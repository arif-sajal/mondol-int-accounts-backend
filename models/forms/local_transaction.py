from pydantic import validator
from odmantic.bson import BaseBSONModel, ObjectId
from typing import Optional

# Import Models
from models import TransactionType, TransactionReferenceType

# Import Validators
from validators.form.notEmpty import not_empty


class LocalTransactionForm(BaseBSONModel):
    amount: float
    type: TransactionType
    reference_type: TransactionReferenceType
    reference: ObjectId
    note: Optional[str]
    remark: Optional[str]

    # Validators
    _non_empty_fields = validator('type', 'reference_type', allow_reuse=True)(not_empty)
