from fastapi import APIRouter, Response, status
from odmantic.bson import ObjectId
from typing import List

# Import Models
from models.client import Client, ClientOut

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.options import make as make_options
from helpers.auth import Auth

# Import Forms
from models.forms.client import CreateClientForm, UpdateClientForm, ChangeClientPasswordForm

# Import Validators
from validators.form.countryExists import country_exists

# Import Responses
from models.response.client import ClientsPaginatedResults, ClientResponse
from models.response.common import ErrorResponse, NotFound

# Import Utils
import datetime

api = APIRouter(
    prefix='/v1/client',
    tags=["Clients"]
)


@api.post(
    '/get-paginated',
    description='Get clients with or without advanced filters.',
    responses={
        200: {'model': ClientsPaginatedResults}
    }
)
async def get_paginated_clients(pagination: PaginationParameters):
    results = await prepare_result(ClientOut, pagination)
    return results


@api.get(
    '/get-as-options',
    description='Get clients with filters as options.',
    responses={
        200: {'model': List[ClientOut]}
    }
)
async def get_client_options(query: str = ''):
    results = await make_options(ClientOut, ['name', 'email', 'username', 'phone'], query)
    return results


@api.get(
    '/get/{cid}',
    description='Get Single client.',
    responses={
        200: {'model': ClientResponse},
        404: {'model': NotFound}
    }
)
async def get_single_client(cid: ObjectId, response: Response):
    client = await db.find_one(Client, Client.id == cid)
    if client is not None:
        return ClientOut(**client.dict())

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'client'],
        msg='Country Not Found'
    )


@api.post(
    '/create',
    description='Create new client.',
    responses={
        200: {'model': ClientResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_client(ccf: CreateClientForm, response: Response):
    country = await country_exists(ccf.country)

    auth = Auth()
    client = Client(
        name=ccf.name,
        email=ccf.email,
        phone=ccf.phone,
        username=ccf.username,
        password=auth.encode_password(ccf.password),
        country=country
    )

    try:
        await db.save(client)
        return ClientResponse(
            loc=['create', 'client', 'success'],
            msg='Client created successfully.',
            data=ClientOut(**client.dict())
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'client', 'error'],
            msg='Can\'t create client now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{cid}',
    description='Update client.',
    responses={
        200: {'model': ClientResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def update_client(cid: ObjectId, ucf: UpdateClientForm, response: Response):
    country = await country_exists(ucf.country)
    client = await db.find_one(Client, Client.id == cid)

    if client is not None:
        client.name = ucf.name
        client.email = ucf.email
        client.phone = ucf.phone
        client.username = ucf.username
        client.country = country
        client.updated_at = datetime.datetime.utcnow()

        try:
            await db.save(client)
            return ClientResponse(
                loc=['update', 'client', 'success'],
                msg='Client updated successfully.',
                data=ClientOut(**client.dict())
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'client', 'error'],
                msg='Can\'t update client now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['client', 'not', 'found'],
        msg='Client not found with the provided ID.'
    )


@api.patch(
    '/change-password/{cid}',
    description='Change client password.',
    responses={
        200: {'model': ClientResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def change_client_password(cid: ObjectId, ccp: ChangeClientPasswordForm, response: Response):
    auth = Auth()
    client = await db.find_one(Client, Client.id == cid)

    if client is not None:
        client.password = auth.encode_password(ccp.password)
        try:
            await db.save(client)
            return ClientResponse(
                loc=['update', 'client', 'success'],
                msg='Client password changed successfully.',
                data=ClientOut(**client.dict())
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'client', 'error'],
                msg='Can\'t update client now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['client', 'not', 'found'],
        msg='Client not found with the provided ID.'
    )


@api.get(
    '/change-status/{cid}',
    description='Change client status.',
    responses={
        200: {'model': ClientResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def change_client_status(cid: ObjectId, response: Response):
    client = await db.find_one(Client, Client.id == cid)

    if client is not None:
        client.status = not client.status

        try:
            await db.save(client)
            return ClientResponse(
                loc=['update', 'client', 'success'],
                msg='Client status changed successfully.',
                data=ClientOut(**client.dict())
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'client', 'error'],
                msg='Can\'t change client status now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['client', 'not', 'found'],
        msg='Client not found with the provided ID.'
    )


@api.delete(
    '/delete/{cid}',
    description='Delete client.',
    responses={
        200: {'model': ClientResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def delete_client(cid: ObjectId, response: Response):
    client = await db.find_one(Client, Client.id == cid)

    if client is not None:
        try:
            await db.delete(client)
            return ClientResponse(
                loc=['delete', 'client', 'success'],
                msg='Client deleted successfully.',
                data=ClientOut(**client.dict())
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'client', 'error'],
                msg='Can\'t delete client now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['client', 'not', 'found'],
        msg='Client not found with the provided ID.'
    )
