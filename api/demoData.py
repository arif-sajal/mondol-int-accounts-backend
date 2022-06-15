from fastapi import APIRouter, Depends

# Import Models
from models.country import Country
from models.currency import Currency
from models.role import Role
from models.admin import Admin
from models.client import Client
from models.response.demoData import DemoDataResponse

# Import Helpers
from helpers.auth import Auth
from helpers.database import db
from helpers.role import Role as RoleHelper
from bcrypt import hashpw, gensalt

api = APIRouter(
    prefix='/v1/demo-data',
    tags=["Demo Data"],
    dependencies=[Depends(Auth().wrapper)]
)


@api.get('/purge', response_model=DemoDataResponse, description='Delete all data from database.')
async def purge_database():

    admins = await db.find(Admin)
    for admin in admins:
        await db.delete(admin)

    roles = await db.find(Role)
    for role in roles:
        await db.delete(role)

    clients = await db.find(Client)
    for client in clients:
        await db.delete(client)

    countries = await db.find(Country)
    for country in countries:
        await db.delete(country)

    currencies = await db.find(Currency)
    for currency in currencies:
        await db.delete(currency)

    return {'loc': ['demo-data', 'purge'], 'message': 'Database Purged Successfully.'}


@api.get('/import-countries', response_model=DemoDataResponse, description='Delete previous Countries and import new countries.')
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


@api.get('/import-currencies', response_model=DemoDataResponse, description='Delete previous currencies and import new currencies.')
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


@api.get('/import-roles', response_model=DemoDataResponse, description='Delete previous Roles and import new roles.')
async def import_roles():
    prev_roles = await db.find(Admin)
    for role in prev_roles:
        await db.delete(role)

    role = RoleHelper()

    super_admin = role.get_super_admin_role()
    roles = role.get_random_roles(5)
    roles.append(super_admin)

    await db.save_all(roles)
    return {'loc': ['demo-data', 'roles'], 'message': 'Roles Imported Successfully'}


@api.get('/import-admins', response_model=DemoDataResponse, description='Delete previous Admins and import new admins.')
async def import_admins():
    prev_admins = await db.find(Admin)
    for admin in prev_admins:
        await db.delete(admin)

    super_admin_role = await db.find_one(Role, Role.name == 'Super Admin')
    random_role = await db.find_one(Role)

    admins = [
        Admin(name='Admin', email="admin@admin.com", phone='+8801908088977', username='admin',
              password=hashpw('123456'.encode('utf-8'), gensalt()), role=super_admin_role),
        Admin(name='Arif Sajal', phone='+8801954465596', email="sajalarifulislam@gmail.com", username='arifsajal',
              password=hashpw('123456'.encode('utf-8'), gensalt()), role=random_role),
    ]

    await db.save_all(admins)
    return {'loc': ['demo-data', 'admins'], 'message': 'Admins Imported Successfully'}


@api.get('/import-clients', response_model=DemoDataResponse, description='Delete previous Clients and import new clients.')
async def import_clients():
    prev_clients = await db.find(Client)
    for client in prev_clients:
        await db.delete(client)

    first_country = await db.find_one(Country)
    second_country = await db.find_one(Country)

    clients = [
        Client(name='Client', email="client@client.com", phone='+8801908088977', username='client', password=hashpw('123456'.encode('utf-8'), gensalt()), country=first_country),
        Client(name='Arif Sajal', email="sajalarifulislam@gmail.com", phone='+8801954465596', username='arifsajal', password=hashpw('123456'.encode('utf-8'), gensalt()), country=second_country),
    ]

    await db.save_all(clients)
    return {'loc': ['demo-data', 'clients'], 'message': 'Clients Imported Successfully'}


@api.get('/reset', response_model=DemoDataResponse, description='Delete all data from database and re import all data again.')
async def full_database_reset():
    await purge_database()
    await import_countries()
    await import_currencies()
    await import_roles()
    await import_admins()
    await import_clients()

    return {'loc': ['demo-data', 'reset'], 'message': 'Database Reset Successful.'}
