from odmantic import Model, Field
from typing import Dict, List, Optional

# Import Utils
import datetime


class Permissions(Dict):
    create: Optional[bool]
    read: Optional[bool]
    update: Optional[bool]
    delete: Optional[bool]


class Module(Dict):
    name: str
    permissions: Permissions


class Role(Model):
    name: str
    description: Optional[str]
    active: bool = True
    modules: List[Module]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main Role Model'
        collection = "roles"


class RoleOut(Model):
    name: str
    description: Optional[str]
    active: bool = True

    class Config:
        title = 'Simple Role Model'
        collection = "roles"
