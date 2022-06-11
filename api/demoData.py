from fastapi import APIRouter

# Import Models
from models.country import Country
from models.currency import Currency
from models.admin import Admin
from models.response.demoData import DemoDataResponse

# Import Helpers
from helpers.database import db
from bcrypt import hashpw, gensalt

api = APIRouter(
    prefix='/v1/demo-data',
    tags=["Demo Data"]
)


@api.get('/purge', response_model=DemoDataResponse)
async def import_currencies():

    countries = await db.find(Country)
    for country in countries:
        await db.delete(country)

    currencies = await db.find(Currency)
    for currency in currencies:
        await db.delete(currency)

    return {'loc': ['demo-data', 'purge'], 'message': 'Database Purge Successfully.'}


@api.get('/import-countries', response_model=DemoDataResponse)
async def import_countries():
    prev_countries = await db.find(Country)
    for country in prev_countries:
        await db.delete(country)

    countries = [
        Country(name='Bangladesh', code="BD"),
        Country(name='India', code="IN"),
        Country(name='United Arab Emirates', code="UAE")
    ]

    await db.save_all(countries)
    return {'loc': ['demo-data', 'countries'], 'message': 'Countries Imported Successfully'}


@api.get('/import-currencies', response_model=DemoDataResponse)
async def import_currencies():
    prev_currencies = await db.find(Currency)
    for currency in prev_currencies:
        await db.delete(currency)

    countries = [
        Currency(name='Bangladeshi Taka', code="BDT", rate=0.00),
        Currency(name='Indian Rupee', code="INR", rate=0.88),
        Currency(name='United Arab Emirates Dirham', code="AED", rate=0.042)
    ]

    await db.save_all(countries)
    return {'loc': ['demo-data', 'currencies'], 'message': 'Currencies Imported Successfully'}


@api.get('/import-admins', response_model=DemoDataResponse)
async def import_currencies():
    prev_admins = await db.find(Admin)
    for admin in prev_admins:
        await db.delete(admin)

    admins = [
        Admin(name='Admin', email="admin@admin.com", username='admin', password=hashpw('123456'.encode('utf-8'), gensalt())),
        Admin(name='Arif Sajal', email="sajalarifulislam@gmail.com", username='arifsajal', password=hashpw('123456'.encode('utf-8'), gensalt())),
    ]

    await db.save_all(admins)
    return {'loc': ['demo-data', 'admins'], 'message': 'Admins Imported Successfully'}
