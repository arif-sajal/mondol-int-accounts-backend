from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import demoData, auth, country, currency, role, admin

description = """

## Items

_Authentication_, _Countries_, _Currencies_, _Roles_, _Admins_, _Clients_

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

* **Read Currencies** (Pagination) (_not implemented_).
* **Read Single Currency** (_not implemented_).
* **Create Currency** (_not implemented_).
* **Update Currency** (_not implemented_).
* **Delete Currency** (_not implemented_).

## Role ⛹

* **Read Roles** (Pagination) (_not implemented_).
* **Read Single Role** (_not implemented_).
* **Create Role** (_not implemented_).
* **Update Role** (_not implemented_).
* **Delete Role** (_not implemented_).
* **Change Role Activation Status** (_not implemented_).

## Admins

* **Read Admins** (Pagination) (_not implemented_).
* **Read Single Admin** (_not implemented_).
* **Create Admin** (_not implemented_).
* **Update Admin** (_not implemented_).
* **Delete Admin** (_not implemented_).
* **Change Admin Password** (_not implemented_).
* **Change Admin Activation Status** (_not implemented_).

## Client

* **Read Clients** (Pagination) (_not implemented_).
* **Read Single Clients** (_not implemented_).
* **Create Client** (_not implemented_).
* **Update Client** (_not implemented_).
* **Delete Client** (_not implemented_).
* **Change Client Password** (_not implemented_).
* **Change Client Status** (_not implemented_).

## Accounts

* **Read Accounts** (Pagination) (_not implemented_).
* **Read Single Account** (_not implemented_).
* **Create Account** (_not implemented_).
* **Update Account** (_not implemented_).
* **Delete Account** (_not implemented_).
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
