from odmantic.bson import BaseBSONModel


class CurrencyForm(BaseBSONModel):
    name: str
    code: str
    rate: float
