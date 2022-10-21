from fastapi import APIRouter, Response, status, Depends
from odmantic.bson import ObjectId
from typing import List

# Import Models
from models.contact import Contact, AdditionalInformation

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.options import make as make_options
from helpers.auth import Auth

# Import Forms
from models.forms.contact import ContactForm

# Import Responses
from models.response.contact import\
    ContactsPaginatedResults,\
    ContactResponse
from models.response.common import ErrorResponse, NotFound

api = APIRouter(
    prefix='/v1/contact',
    tags=["Contacts"],
    dependencies=[Depends(Auth().wrapper)]
)


@api.post(
    '/get-paginated',
    description='Get contacts with or without advanced filters.',
    responses={
        200: {'model': ContactsPaginatedResults}
    }
)
async def get_paginated_contacts(pagination: PaginationParameters):
    results = await prepare_result(Contact, pagination)
    return results


@api.get(
    '/get-as-options',
    description='Get countries with filters as options.',
    responses={
        200: {'model': List[Contact]}
    }
)
async def get_contact_options(query: str = ''):
    results = await make_options(Contact, ['name', 'phone'], query)
    return results


@api.get(
    '/get/{cid}',
    description='Get Single contact.',
    responses={
        200: {'model': Contact},
        404: {'model': NotFound}
    }
)
async def get_single_contact(cid: ObjectId, response: Response):
    contact = await db.find_one(Contact, Contact.id == cid)
    if contact is not None:
        return contact

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'contact'],
        msg='Contact Not Found'
    )


@api.post(
    '/create',
    description='Create new Contact.',
    responses={
        200: {'model': ContactResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_contact(cou: ContactForm, response: Response):
    afs = []
    if len(cou.af) > 0:
        for af in cou.af:
            afs.append(AdditionalInformation(
                key=af.key,
                value=af.value
            ))

    contact = Contact(
        name=cou.name,
        number=cou.number,
        email=cou.email,
        af=afs
    )

    try:
        await db.save(contact)
        return ContactResponse(
            loc=['create', 'contact', 'success'],
            msg='Contact created successfully.',
            data=contact
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'contact', 'error'],
            msg='Can\'t create contact now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{cid}',
    description='Update contact.',
    responses={
        200: {'model': ContactResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def update_contact(cid: ObjectId, cou: ContactForm, response: Response):
    contact = await db.find_one(Contact, Contact.id == cid)

    if contact is not None:
        afs = []
        if len(cou.af) > 0:
            for af in cou.af:
                afs.append(AdditionalInformation(
                    key=af.key,
                    value=af.value
                ))

        contact.name = cou.name
        contact.number = cou.number
        contact.email = cou.email
        contact.af = afs

        try:
            await db.save(contact)
            return ContactResponse(
                loc=['update', 'contact', 'success'],
                msg='Contact updated successfully.',
                data=contact
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'contact', 'error'],
                msg='Can\'t update contact now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['contact', 'not', 'found'],
        msg='Contact not found with the provided ID.'
    )


@api.delete(
    '/delete/{cid}',
    description='Delete Contact.',
    responses={
        200: {'model': ContactResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def delete_contact(cid: ObjectId, response: Response):
    contact = await db.find_one(Contact, Contact.id == cid)

    if contact is not None:
        try:
            await db.delete(contact)
            return ContactResponse(
                loc=['delete', 'contact', 'success'],
                msg='Contact deleted successfully.',
                data=contact
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'contact', 'error'],
                msg='Can\'t delete contact now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['contact', 'not', 'found'],
        msg='Contact not found with the provided ID.'
    )
