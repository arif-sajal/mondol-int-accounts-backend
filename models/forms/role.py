from pydantic import validator
from odmantic.bson import BaseBSONModel
from typing import Optional
from typing_extensions import TypedDict

# Import Validators
from validators.form.notEmpty import not_empty


class Permissions(TypedDict, total=False):
    create: Optional[bool]
    read: Optional[bool]
    update: Optional[bool]
    delete: Optional[bool]


class Modules(TypedDict):
    dashboard: Permissions
    role: Permissions
    admin: Permissions
    client: Permissions
    local_transaction: Permissions
    foreign_transaction: Permissions
    country: Permissions
    currency: Permissions
    account: Permissions
    contact: Permissions


class RoleForm(BaseBSONModel):
    name: str
    description: str
    modules: Modules

    # Validators
    _not_empty_name = validator('name', allow_reuse=True)(not_empty)
