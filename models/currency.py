from odmantic import Model


class Currency(Model):
    name: str
    code: str
    rate: float

    class Config:
        title = 'Main Currency Model'
        collection = "currencies"
