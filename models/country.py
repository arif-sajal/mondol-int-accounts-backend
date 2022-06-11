from odmantic import Model


class Country(Model):
    name: str
    code: str

    class Config:
        title = 'Main Country Model'
        collection = "countries"
