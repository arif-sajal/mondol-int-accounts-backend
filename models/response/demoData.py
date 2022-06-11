from odmantic.model import BaseModel


class DemoDataResponse(BaseModel):
    loc: list
    message: str
