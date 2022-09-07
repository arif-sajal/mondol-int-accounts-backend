from pydantic import validator
from typing import Optional
from odmantic.bson import BaseBSONModel, ObjectId

# Import Validators
from validators.form.notEmpty import not_empty


class AccountForm(BaseBSONModel):
    name: str
    description: str
    currency: ObjectId
    balance: Optional[float]

    # Validators
    _non_empty_fields = validator('name', 'description', 'currency', allow_reuse=True)(not_empty)
