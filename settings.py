from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = 'Mondol International Accounting'
    APP_SECRET: str = '671a862f961ae7b705db1a33480ade5ef31fd45476186164b6189471421bb0f0'
    APP_ALGORITHM: str = 'HS256'
    DEBUG_MODE: bool = True
    ENVIRONMENT: str = 'dev'
    LOCAL_CURRENCY: str = 'BDT'
    LOCAL_COUNTRY: str = 'BD'


class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    # DB_URL: str = f'mongodb+srv://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@{os.getenv("MONGO_HOSTNAME")}'
    # DB_NAME: str = os.getenv("MONGO_DBNAME")
    DB_URL: str = f'mongodb+srv://bbazaar:sajals70@bbazaar.uawcu.mongodb.net/?retryWrites=true&w=majority'
    DB_NAME: str = 'mi-back'


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
