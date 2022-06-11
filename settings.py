from pydantic import BaseSettings
import os


class CommonSettings(BaseSettings):
    APP_NAME: str = 'Mondol International Accounting'
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    # DB_URL: str = f'mongodb+srv://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@{os.getenv("MONGO_HOSTNAME")}'
    DB_URL: str = f'mongodb+srv://bbazaar:sajals70@bbazaar.uawcu.mongodb.net/?retryWrites=true&w=majority'
    DB_NAME: str = os.getenv("MONGO_DBNAME")


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
