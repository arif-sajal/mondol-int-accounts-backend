from odmantic import Model, Field

# Import Utils
import datetime


class Currency(Model):
    name: str
    code: str
    symbol: str
    rate: float
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main Currency Model'
        collection = "currencies"
