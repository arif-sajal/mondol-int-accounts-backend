from odmantic.bson import BaseBSONModel


class CountryForm(BaseBSONModel):
    name: str
    code: str
