from odmantic import Model
from typing import Dict, List, Optional


class Permissions(Dict):
    create: Optional[bool]
    read: bool = False
    update: Optional[bool]
    delete: Optional[bool]


class Module(Dict):
    name: str
    permissions: Permissions


class Role(Model):
    name: str
    modules: List[Module]

    class Config:
        collection = "roles"
