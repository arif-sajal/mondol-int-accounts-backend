from odmantic.bson import BaseBSONModel


class CreateCurrencyForm(BaseBSONModel):
    name: str
    code: str
    symbol: str
    rate: float
    balance: float


class UpdateCurrencyForm(BaseBSONModel):
    name: str
    code: str
    symbol: str
    rate: float
