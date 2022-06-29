from odmantic.bson import BaseBSONModel
from typing import Optional
from typing_extensions import TypedDict


class Permissions(TypedDict):
    create: Optional[bool]
    read: Optional[bool]
    update: Optional[bool]
    delete: Optional[bool]


class Modules(TypedDict):
    dashboard: Permissions
    role: Permissions
    admin: Permissions
    client: Permissions
    country: Permissions
    currency: Permissions
    account: Permissions


class RoleForm(BaseBSONModel):
    name: str
    modules: Modules
