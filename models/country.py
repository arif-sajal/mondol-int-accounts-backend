from odmantic import Model, Field

# Import Utils
import datetime


class Country(Model):
    name: str
    code: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        title = 'Main Country Model'
        collection = "countries"
