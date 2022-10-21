import datetime

from fastapi import APIRouter
from settings import settings

# Import Models
from models import TransactionType
from models.country import Country
from models.currency import Currency
from models.role import Role
from models.admin import Admin
from models.client import Client
from models.account import Account
from models.local_transaction import LocalTransaction
from models.foreign_transaction import ForeignTransaction
from models.response.demoData import DemoDataResponse

# Import Helpers
from helpers.auth import Auth
from helpers.database import db
from helpers.role import Role as RoleHelper

# Import Utils
from faker import Faker

api = APIRouter(
    prefix='/v1/demo-data',
    tags=["Demo Data"]
)


@api.get('/purge', response_model=DemoDataResponse, description='Delete all data from database.')
async def purge_database():
    admins = await db.find(Admin)
    for admin in admins:
        await db.delete(admin)

    roles = await db.find(Role)
    for role in roles:
        await db.delete(role)

    local_transactions = await db.find(LocalTransaction)
    for lt in local_transactions:
        await lt.delete_ledger()
        await db.delete(lt)

    foreign_transactions = await db.find(ForeignTransaction)
    for ft in foreign_transactions:
        await ft.delete_ledger()
        await db.delete(ft)

    clients = await db.find(Client)
    for client in clients:
        await db.delete(client)

    accounts = await db.find(Account)
    for account in accounts:
        await db.delete(account)

    countries = await db.find(Country)
    for country in countries:
        await db.delete(country)

    currencies = await db.find(Currency)
    for currency in currencies:
        await db.delete(currency)

    return {'loc': ['demo-data', 'purge'], 'msg': 'Database Purged Successfully.'}


@api.get('/import-countries', response_model=DemoDataResponse,
         description='Delete previous Countries and import new countries.')
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
    return {'loc': ['demo-data', 'countries'], 'msg': 'Countries Imported Successfully'}


@api.get('/import-currencies', response_model=DemoDataResponse,
         description='Delete previous currencies and import new currencies.')
async def import_currencies():
    prev_currencies = await db.find(Currency)
    for currency in prev_currencies:
        await db.delete(currency)

    countries = [
        Currency(name='Bangladeshi Taka', code="BDT", rate=1.00, symbol='৳'),
        Currency(name='Indian Rupee', code="INR", rate=0.77, symbol='₹'),
        Currency(name='United Arab Emirates Dirham', code="AED", rate=0.035, symbol='د.إ')
    ]

    await db.save_all(countries)
    return {'loc': ['demo-data', 'currencies'], 'msg': 'Currencies Imported Successfully'}


@api.get('/import-roles', response_model=DemoDataResponse, description='Delete previous Roles and import new roles.')
async def import_roles():
    prev_roles = await db.find(Admin)
    for role in prev_roles:
        await db.delete(role)

    role = RoleHelper()
    roles = list()

    if settings.ENVIRONMENT == 'dev':
        roles += role.get_random_roles(15)

    super_admin = role.get_super_admin_role()
    roles.append(super_admin)

    await db.save_all(roles)
    return {'loc': ['demo-data', 'roles'], 'msg': 'Roles Imported Successfully'}


@api.get('/import-admins', response_model=DemoDataResponse, description='Delete previous Admins and import new admins.')
async def import_admins():
    prev_admins = await db.find(Admin)
    for admin in prev_admins:
        await db.delete(admin)

    super_admin_role = await db.find_one(Role, Role.name == 'Super Admin')
    random_role = await db.find_one(Role)
    auth = Auth()

    admins = [
        Admin(name='Admin', email="admin@admin.com", phone='+8801908088977', username='admin', status=True,
              password=auth.encode_password('123456'), role=super_admin_role),
        Admin(name='Arif Sajal', phone='+8801954465596', email="sajalarifulislam@gmail.com", username='arifsajal',
              status=True, password=auth.encode_password('123456'), role=random_role),
    ]

    await db.save_all(admins)
    return {'loc': ['demo-data', 'admins'], 'msg': 'Admins Imported Successfully'}


@api.get('/import-clients', response_model=DemoDataResponse,
         description='Delete previous Clients and import new clients.')
async def import_clients():
    prev_clients = await db.find(Client)
    for client in prev_clients:
        await db.delete(client)

    country = await db.find_one(Country)
    first_currency = await db.find_one(Currency, Currency.code == 'BDT')
    second_currency = await db.find_one(Currency, Currency.code == 'INR')
    auth = Auth()

    clients = [
        Client(name='Client', email="client@client.com", phone='+8801908088977', username='client',
               password=auth.encode_password('123456'), status=True, country=country, currency=first_currency),
        Client(name='Arif Sajal', email="sajalarifulislam@gmail.com", phone='+8801954465596', username='arifsajal',
               password=auth.encode_password('123456'), status=True, country=country, currency=second_currency),
    ]

    await db.save_all(clients)
    return {'loc': ['demo-data', 'clients'], 'msg': 'Clients Imported Successfully'}


@api.get('/import-accounts', response_model=DemoDataResponse,
         description='Delete previous Accounts and import new accounts.')
async def import_accounts():
    prev_accounts = await db.find(Account)
    for account in prev_accounts:
        await db.delete(account)

    if settings.ENVIRONMENT == 'dev':
        fake = Faker()
        accounts = list()
        for _ in range(5):
            accounts.append(Account(
                name=fake.catch_phrase(),
                description=fake.credit_card_full(),
                balance=fake.pyfloat(positive=True)
            ))
        await db.save_all(accounts)

    return {'loc': ['demo-data', 'accounts'], 'msg': 'Accounts Imported Successfully'}


@api.get('/import-local-transactions', response_model=DemoDataResponse,
         description='Delete previous Local Transactions and import new local transactions.')
async def import_local_transactions():
    prev_local_transactions = await db.find(LocalTransaction)
    for lc in prev_local_transactions:
        await db.delete(lc)

    if settings.ENVIRONMENT == 'dev':
        fake = Faker()
        transactions = list()
        accounts = await db.find(Account)
        clients = await db.find(Client)
        transaction_types = TransactionType
        to_currency = await db.find_one(Currency, Currency.code == settings.LOCAL_CURRENCY)

        for _ in range(250):
            tr_type = fake.random_element(elements=transaction_types)
            account = fake.random_element(elements=accounts)
            client = fake.random_element(elements=clients)
            amount = fake.pyint(min_value=500, max_value=1000000)
            ad_rate = round(client.currency.rate / to_currency.rate, 3)
            ad_amount = round(ad_rate * amount)

            client_balance = 0
            client_ad_balance = 0

            if tr_type == TransactionType.PAID:
                client_balance = client.balance + amount
                client_ad_balance = client.ad_balance + ad_amount

            if tr_type == TransactionType.RECEIVED:
                client_balance = client.balance - amount
                client_ad_balance = client.ad_balance - ad_amount

            transactions.append(LocalTransaction(
                amount=amount,
                type=tr_type,
                account=account,
                client=client,
                ad_currency=client.currency,
                ad_rate=ad_rate,
                ad_amount=ad_amount,
                client_balance=client_balance,
                client_ad_balance=client_ad_balance,
                note=fake.text(max_nb_chars=25),
                remark=fake.text(max_nb_chars=25)
            ))

        await db.save_all(transactions)

        transactions = await db.find(LocalTransaction)
        for transaction in transactions:
            await transaction.create_ledger()

    return {'loc': ['demo-data', 'accounts'], 'msg': 'Local Transactions Imported Successfully'}


@api.get('/import-foreign-transactions', response_model=DemoDataResponse,
         description='Delete previous Foreign Transactions and import new foreign transactions.')
async def import_foreign_transactions():
    prev_foreign_transactions = await db.find(ForeignTransaction)
    for fc in prev_foreign_transactions:
        await db.delete(fc)

    if settings.ENVIRONMENT == 'dev':
        fake = Faker()
        transactions = list()
        clients = await db.find(Client)
        transaction_types = TransactionType
        currencies = await db.find(Currency, Currency.code != settings.LOCAL_CURRENCY)
        to_currency = await db.find_one(Currency, Currency.code == settings.LOCAL_CURRENCY)

        for _ in range(250):
            tr_type = fake.random_element(elements=transaction_types)
            client = fake.random_element(elements=clients)
            from_currency = fake.random_element(elements=currencies)

            rate = round(to_currency.rate / from_currency.rate, 3)
            amount = fake.pyint(min_value=500, max_value=1000000)
            cv_amount = round(amount * rate, 2)

            if client.currency.id != to_currency.id:
                ad_currency = client.currency
                ad_rate = round(ad_currency.rate / to_currency.rate, 3)
                ad_cv_amount = round(cv_amount * ad_rate, 3)
            else:
                ad_currency = to_currency
                ad_rate = 1.00
                ad_cv_amount = cv_amount

            client_balance = 0
            client_ad_balance = 0

            if tr_type == TransactionType.PAID:
                client_balance = client.balance + cv_amount
                client_ad_balance = client.ad_balance + ad_cv_amount

            if tr_type == TransactionType.RECEIVED:
                client_balance = client.balance - cv_amount
                client_ad_balance = client.ad_balance - ad_cv_amount

            transactions.append(ForeignTransaction(
                from_currency=from_currency,
                to_currency=to_currency,
                rate=rate,
                amount=amount,
                cv_amount=round(amount * rate, 2),
                type=tr_type,
                client=client,
                ad_currency=ad_currency,
                ad_rate=ad_rate,
                ad_cv_amount=ad_cv_amount,
                client_balance=client_balance,
                client_ad_balance=client_ad_balance,
                note=fake.text(max_nb_chars=25),
                remark=fake.text(max_nb_chars=25)
            ))

        await db.save_all(transactions)

        transactions = await db.find(ForeignTransaction)
        for transaction in transactions:
            await transaction.create_ledger()

    return {'loc': ['demo-data', 'accounts'], 'msg': 'Foreign Transactions Imported Successfully'}


@api.get('/reset', response_model=DemoDataResponse,
         description='Delete all data from database and re import all data again.')
async def full_database_reset():
    await purge_database()
    await import_countries()
    await import_currencies()
    await import_roles()
    await import_admins()
    await import_clients()
    await import_accounts()
    await import_local_transactions()
    await import_foreign_transactions()

    return {'loc': ['demo-data', 'reset'], 'msg': 'Database Reset Successful.'}
