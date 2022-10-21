from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import demoData, auth, country, currency, role, admin, client, account, local_transaction, foreign_transaction, contact

description = """

## Items

_Authentication_, _Countries_, _Currencies_, _Roles_, _Admins_, _Clients_, _Accounts_, _Local Transactions_, _Foreign Transactions_

## Authentication 🔐

* **Login** With Credential (_Implemented_).
* Request OTP For **Login** With Phone (_Implemented_).
* **Login** With Phone (_Implemented_).
* Request **Reset Password** OTP (_Implemented_).
* Verify **Reset Password** OTP (_Implemented_).
* **Reset Password** (_Implemented_).

## Countries 🌍

* **Read Countries** (Pagination) (_Implemented_).
* **Read Country Options** (_Implemented_).
* **Read Single Country** (_Implemented_).
* **Create Country** (_Implemented_).
* **Update Country** (_Implemented_).
* **Delete Country** (_Implemented_).

## Currencies 💸

* **Read Currencies** (Pagination) (_Implemented_).
* **Read Currencies Options** (_Implemented_).
* **Read Single Currency** (_Implemented_).
* **Create Currency** (_Implemented_).
* **Update Currency** (_Implemented_).
* **Delete Currency** (_Implemented_).

## Role ⛹

* **Read Roles** (Pagination) (_Implemented_).
* **Read Roles Options** (_Implemented_).
* **Read Single Role** (_Implemented_).
* **Create Role** (_Implemented_).
* **Update Role** (_Implemented_).
* **Delete Role** (_Implemented_).
* **Change Role Activation Status** (_Implemented_).

## Admins

* **Read Admins** (Pagination) (_Implemented_).
* **Read Admins Options** (_Implemented_).
* **Read Single Admin** (_Implemented_).
* **Create Admin** (_Implemented_).
* **Update Admin** (_Implemented_).
* **Delete Admin** (_Implemented_).
* **Change Admin Password** (_Implemented_).
* **Change Admin Activation Status** (_Implemented_).

## Client

* **Read Clients** (Pagination) (_Implemented_).
* **Read Clients Options** (_Implemented_).
* **Read Single Clients** (_Implemented_).
* **Create Client** (_Implemented_).
* **Update Client** (_Implemented_).
* **Delete Client** (_Implemented_).
* **Change Client Password** (_Implemented_).
* **Change Client Activation Status** (_Implemented_).

## Accounts

* **Read Accounts** (Pagination) (_Implemented_).
* **Read Accounts Options** (_Implemented_).
* **Read Single Account** (_Implemented_).
* **Create Account** (_Implemented_).
* **Update Account** (_Implemented_).
* **Delete Account** (_Implemented_).
* **Change Account Activation Status** (_Implemented_).

## Local Transaction

* **Read Local Transactions** (Pagination) (_Implemented_).
* **Read Single Local Transaction** (_Implemented_).
* **Create Local Transaction** (_Implemented_).
* **Update Local Transaction** (_Implemented_).
* **Delete Local Transaction** (_Implemented_).

## Foreign Transaction

* **Read Foreign Transaction** (Pagination) (_Implemented_).
* **Read Single Foreign Transaction** (_Implemented_).
* **Create Foreign Transaction** (_Implemented_).
* **Update Foreign Transaction** (_Implemented_).
* **Delete Foreign Transaction** (_Implemented_).

## Contact

* **Read Contact** (Pagination) (_Implemented_).
* **Read Single Contact** (_Implemented_).
* **Create Contact** (_Implemented_).
* **Update Contact** (_Implemented_).
* **Delete Contact** (_Implemented_).
"""

tags_metadata = [
    {
        "name": "Demo Data",
        "description": "Demo Data Management to populate the **Database** with demo data.",
    },
    {
        "name": "Authentication",
        "description": "Authentication For Admin and Clients.",
    },
    {
        "name": "Countries",
        "description": "Operations with **Countries**."
    },
    {
        "name": "Currencies",
        "description": "Operations with **Countries**."
    },
    {
        "name": "Roles",
        "description": "Operations with **Roles**."
    },
    {
        "name": "Admins",
        "description": "Operations with **Admins**."
    },
    {
        "name": "Clients",
        "description": "Operations with **Admins**."
    },
    {
        "name": "Accounts",
        "description": "Operations with **Accounts**."
    },
    {
        "name": "Local Transaction",
        "description": "Operations with **local transactions**."
    },
    {
        "name": "Foreign Transaction",
        "description": "Operations with **foreign transactions**."
    },
    {
        "name": "Contact",
        "description": "Operations with **contacts**."
    }
]

app = FastAPI(
    title='M.I.A. Backend API Endpoints',
    version='0.0.1',
    description=description,
    openapi_tags=tags_metadata,
    contact={
        "name": "Arif Sajal",
        "email": "sajalarifulislam@gmail.com",
    }
)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(demoData.api)
app.include_router(auth.api)
app.include_router(country.api)
app.include_router(currency.api)
app.include_router(role.api)
app.include_router(admin.api)
app.include_router(client.api)
app.include_router(account.api)
app.include_router(local_transaction.api)
app.include_router(foreign_transaction.api)
app.include_router(contact.api)
