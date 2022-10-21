from odmantic import Model, Field

# Import Utils
import datetime


class Account(Model):
    name: str
    description: str
    balance: float = Field(default=0.0)
    status: bool = Field(default=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main account model for internal use.'
        collection = "accounts"
