from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import demoData

description = """
SaaS Pos **Utility** API helps managing **utilities**.

## Items

_Countries_, _Currencies_

## Countries

* **Read Countries** (Pagination - Optional) (_not implemented_).
* **Read Single Country** (_not implemented_).
* **Create Country** (_not implemented_).
* **Update Country** (_not implemented_).
* **Delete Country** (_not implemented_).

## Currencies

* **Read Currencies** (Pagination - Optional) (_not implemented_).
* **Read Single Currency** (Pagination - Optional) (_not implemented_).
* **Create Currency** (_not implemented_).
* **Update Currency** (_not implemented_).
* **Delete Currency** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "Demo Data",
        "description": "Demo Data Management to manage the **Database**.",
    },
    {
        "name": "Countries",
        "description": "Operations with **Countries**."
    },
    {
        "name": "Currencies",
        "description": "Operations with **Countries**."
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


app.include_router(demoData.api)
