import datetime

from fastapi import APIRouter
from settings import settings

# Import Models
from models import TransactionType, TransactionReferenceType
from models.country import Country
from models.currency import Currency
from models.role import Role
from models.admin import Admin
from models.client import Client
from models.balance import Balance
from models.account import Account
from models.local_transaction import LocalTransaction
from models.foreign_transaction import ForeignTransaction
from models.response.demoData import DemoDataResponse

# Import Helpers
from helpers.auth import Auth
from helpers.database import db
from helpers.role import Role as RoleHelper
from helpers.balance import Balance as BalanceHelp

# Import Utils
from faker import Faker


api = APIRouter(
    prefix='/v1/demo-data',
    tags=["Demo Data"],
    dependencies=[]
)


@api.get('/purge', response_model=DemoDataResponse, description='Delete all data from database.')
async def purge_database():

    admins = await db.find(Admin)
    for admin in admins:
        await db.delete(admin)

    roles = await db.find(Role)
    for role in roles:
        await db.delete(role)

    balances = await db.find(Balance)
    for balance in balances:
        await db.delete(balance)

    local_transactions = await db.find(LocalTransaction)
    for lt in local_transactions:
        await db.delete(lt)

    foreign_transactions = await db.find(ForeignTransaction)
    for ft in foreign_transactions:
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
    return {'loc': ['demo-data', 'countries'], 'msg': 'Countries Imported Successfully'}


@api.get('/import-currencies', response_model=DemoDataResponse, description='Delete previous currencies and import new currencies.')
async def import_currencies():
    prev_currencies = await db.find(Currency)
    for currency in prev_currencies:
        await db.delete(currency)

    countries = [
        Currency(name='Bangladeshi Taka', code="BDT", rate=0.00, symbol='৳'),
        Currency(name='Indian Rupee', code="INR", rate=0.88, symbol='₹'),
        Currency(name='United Arab Emirates Dirham', code="AED", rate=0.042, symbol='د.إ')
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


@api.get('/import-clients', response_model=DemoDataResponse, description='Delete previous Clients and import new clients.')
async def import_clients():
    prev_clients = await db.find(Client)
    for client in prev_clients:
        await db.delete(client)

    first_country = await db.find_one(Country)
    second_country = await db.find_one(Country)
    auth = Auth()

    clients = [
        Client(name='Client', email="client@client.com", phone='+8801908088977', username='client', password=auth.encode_password('123456'), status=True, country=first_country),
        Client(name='Arif Sajal', email="sajalarifulislam@gmail.com", phone='+8801954465596', username='arifsajal', password=auth.encode_password('123456'), status=True, country=second_country),
    ]

    await db.save_all(clients)
    return {'loc': ['demo-data', 'clients'], 'msg': 'Clients Imported Successfully'}


@api.get('/import-balances', response_model=DemoDataResponse, description='Delete previous balances and import new balances.')
async def import_balances():
    prev_balances = await db.find(Balance)
    for balance in prev_balances:
        await db.delete(balance)

    if settings.ENVIRONMENT == 'dev':
        balances = list()
        clients = await db.find(Client)
        currencies = await db.find(Currency)
        for client in clients:
            for currency in currencies:
                balances.append(Balance(
                    client=client,
                    currency=currency
                ))
        await db.save_all(balances)

    return {'loc': ['demo-data', 'balances'], 'msg': 'Balances Imported Successfully'}


@api.get('/import-accounts', response_model=DemoDataResponse, description='Delete previous Accounts and import new accounts.')
async def import_accounts():
    prev_accounts = await db.find(Account)
    for account in prev_accounts:
        await db.delete(account)

    if settings.ENVIRONMENT == 'dev':
        fake = Faker()
        accounts = list()
        currencies = await db.find(Currency)
        for _ in range(15):
            accounts.append(Account(
                name=fake.catch_phrase(),
                description=fake.credit_card_full(),
                currency=fake.random_element(elements=currencies),
                balance=fake.pyfloat(positive=True)
            ))
        await db.save_all(accounts)

    return {'loc': ['demo-data', 'accounts'], 'msg': 'Accounts Imported Successfully'}


@api.get('/import-local-transactions', response_model=DemoDataResponse, description='Delete previous Local Transactions and import new local transactions.')
async def import_local_transactions():
    prev_local_transactions = await db.find(LocalTransaction)
    for lc in prev_local_transactions:
        await db.delete(lc)

    if settings.ENVIRONMENT == 'dev':
        fake = Faker()
        transactions = list()
        clients = await db.find(Client)
        accounts = await db.find(Account)
        reference_types = TransactionReferenceType
        transaction_types = TransactionType
        local_currency = await db.find_one(Currency, Currency.code == settings.LOCAL_CURRENCY)

        for _ in range(250):
            rf_type = fake.random_element(elements=reference_types)
            tr_type = fake.random_element(elements=transaction_types)
            rf = rf_type == TransactionReferenceType.ACCOUNT and fake.random_element(elements=accounts) or fake.random_element(elements=clients)
            amount = fake.pyfloat(positive=True, min_value=500, max_value=1000000)

            transactions.append(LocalTransaction(
                amount=amount,
                type=tr_type,
                reference_type=rf_type,
                reference=rf.id,
                note=fake.paragraph(),
                remark=fake.paragraph(),
                created_at=datetime.datetime.now()
            ))

            if rf_type == TransactionReferenceType.ACCOUNT:
                account = rf
                if tr_type == TransactionType.PAID:
                    account.balance = account.balance - amount
                else:
                    account.balance = account.balance + amount
                await db.save(account)

            elif rf_type == TransactionReferenceType.CLIENT:
                balance = await BalanceHelp(client=rf, currency=local_currency).get()

                if tr_type == TransactionType.PAID:
                    balance.balance = balance.balance - amount
                else:
                    balance.balance = balance.balance + amount
                await db.save(balance)

        await db.save_all(transactions)

    return {'loc': ['demo-data', 'accounts'], 'msg': 'Local Transactions Imported Successfully'}


@api.get('/import-foreign-transactions', response_model=DemoDataResponse, description='Delete previous Foreign Transactions and import new foreign transactions.')
async def import_foreign_transactions():
    prev_foreign_transactions = await db.find(ForeignTransaction)
    for fc in prev_foreign_transactions:
        await db.delete(fc)

    if settings.ENVIRONMENT == 'dev':
        fake = Faker()
        transactions = list()
        clients = await db.find(Client)
        accounts = await db.find(Account)
        reference_types = TransactionReferenceType
        transaction_types = TransactionType
        from_currencies = await db.find(Currency, Currency.code == settings.LOCAL_CURRENCY)

        for _ in range(250):
            rf_type = fake.random_element(elements=reference_types)
            tr_type = fake.random_element(elements=transaction_types)
            rf = rf_type == TransactionReferenceType.ACCOUNT and fake.random_element(elements=accounts) or fake.random_element(elements=clients)
            from_currency = fake.random_element(elements=from_currencies)
            to_currencies = await db.find(Currency, Currency.id != from_currency.id)
            to_currency = fake.random_element(elements=to_currencies)

            rate = fake.pyfloat(positive=True, min_value=1.25, max_value=120)
            amount = fake.pyfloat(positive=True, min_value=500, max_value=1000000)

            transactions.append(ForeignTransaction(
                from_currency=from_currency,
                to_currency=to_currency,
                rate=rate,
                amount=amount,
                cv_amount=amount * rate,
                type=tr_type,
                reference_type=rf_type,
                reference=rf.id,
                note=fake.paragraph(),
                remark=fake.paragraph(),
                created_at=datetime.datetime.now()
            ))

            if rf_type == TransactionReferenceType.ACCOUNT:
                account = rf
                if tr_type == TransactionType.PAID:
                    account.balance = account.balance - amount
                else:
                    account.balance = account.balance + amount
                await db.save(account)

            elif rf_type == TransactionReferenceType.CLIENT:
                balance = await BalanceHelp(client=rf, currency=to_currency).get()

                if tr_type == TransactionType.PAID:
                    balance.balance = balance.balance - amount
                else:
                    balance.balance = balance.balance + amount
                await db.save(balance)

        await db.save_all(transactions)

    return {'loc': ['demo-data', 'accounts'], 'msg': 'Foreign Transactions Imported Successfully'}


@api.get('/reset', response_model=DemoDataResponse, description='Delete all data from database and re import all data again.')
async def full_database_reset():
    await purge_database()
    await import_countries()
    await import_currencies()
    await import_roles()
    await import_admins()
    await import_clients()
    await import_balances()
    await import_accounts()
    await import_local_transactions()
    await import_foreign_transactions()

    return {'loc': ['demo-data', 'reset'], 'msg': 'Database Reset Successful.'}
