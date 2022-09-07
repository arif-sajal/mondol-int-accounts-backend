from pydantic import validator
from odmantic.bson import BaseBSONModel, ObjectId

# Import Models
from models import TransactionType, TransactionReferenceType

# Import Validators
from validators.form.notEmpty import not_empty


class ForeignTransactionForm(BaseBSONModel):
    from_currency: ObjectId
    to_currency: ObjectId
    rate: float
    amount: float
    cv_amount: float
    type: TransactionType
    reference_type: TransactionReferenceType
    reference: ObjectId
    note: str
    remark: str

    # Validators
    _non_empty_fields = validator('type', 'reference_type', allow_reuse=True)(not_empty)
