from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import demoData, auth

description = """

## Items

_Authentication_, _Countries_, _Currencies_, _Roles_, _Admins_, _Clients_

## Authentication 🔐

* **Login** With Credential (_not implemented_).
* Request OTP For **Login** With Phone (_not implemented_).
* **Login** With Phone (_not implemented_).
* **Request Reset Password Key** (_not implemented_).
* **Reset Password** (_not implemented_).

## Countries 🌍

* **Read Countries** (Pagination - Optional) (_not implemented_).
* **Read Single Country** (_not implemented_).
* **Create Country** (_not implemented_).
* **Update Country** (_not implemented_).
* **Delete Country** (_not implemented_).

## Currencies 💸

* **Read Currencies** (Pagination - Optional) (_not implemented_).
* **Read Single Currency** (Pagination - Optional) (_not implemented_).
* **Create Currency** (_not implemented_).
* **Update Currency** (_not implemented_).
* **Delete Currency** (_not implemented_).

## Role ⛹

* **Read Roles** (Pagination - Optional) (_not implemented_).
* **Read Single Role** (Pagination - Optional) (_not implemented_).
* **Create Role** (_not implemented_).
* **Update Role** (_not implemented_).
* **Delete Role** (_not implemented_).
* **Change Role Activation Status** (_not implemented_).

## Admins

* **Read Admins** (Pagination - Optional) (_not implemented_).
* **Read Single Admin** (Pagination - Optional) (_not implemented_).
* **Create Admin** (_not implemented_).
* **Update Admin** (_not implemented_).
* **Delete Admin** (_not implemented_).
* **Change Admin Password** (_not implemented_).
* **Change Admin Activation Status** (_not implemented_).

## Client

* **Read Clients** (Pagination - Optional) (_not implemented_).
* **Read Single Clients** (Pagination - Optional) (_not implemented_).
* **Create Clients** (_not implemented_).
* **Update Clients** (_not implemented_).
* **Delete Clients** (_not implemented_).
* **Change Admin Clients** (_not implemented_).
* **Change Admin Clients Status** (_not implemented_).
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
        "name": "Role",
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
]

app = FastAPI(
    title='Mondol International Accounts Backend API Endpoints',
    version='0.0.1',
    description=description,
    openapi_tags=tags_metadata,
    contact={
        "name": "Arif Sajal",
        "email": "sajalarifulislam@gmail.com",
    }
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(demoData.api)
app.include_router(auth.api)
