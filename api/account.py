from fastapi import APIRouter, Response, status, Depends
from odmantic.bson import ObjectId
from typing import List

# Import Models
from models.account import Account

# Import Helpers
from helpers.auth import Auth
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.options import make as make_options

# Import Forms
from models.forms.account import AccountForm

# Import Responses
from models.response.account import AccountsPaginatedResults, AccountResponse
from models.response.common import ErrorResponse, NotFound

# Import Utils
import datetime

api = APIRouter(
    prefix='/v1/account',
    tags=["Accounts"],
    dependencies=[Depends(Auth().wrapper)],
)


@api.post(
    '/get-paginated',
    description='Get accounts with or without advanced filters.',
    responses={
        200: {'model': AccountsPaginatedResults}
    }
)
async def get_paginated_accounts(pagination: PaginationParameters):
    results = await prepare_result(Account, pagination)
    return results


@api.get(
    '/get-as-options',
    description='Get accounts with filters as options.',
    responses={
        200: {'model': List[Account]}
    }
)
async def get_account_options(query: str = ''):
    results = await make_options(Account, ['name'], query)
    return results


@api.get(
    '/get/{aid}',
    description='Get Single account.',
    responses={
        200: {'model': AccountResponse},
        404: {'model': NotFound}
    }
)
async def get_single_account(aid: ObjectId, response: Response):
    account = await db.find_one(Account, Account.id == aid)
    if account is not None:
        return account

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'account'],
        msg='Account Not Found'
    )


@api.post(
    '/create',
    description='Create new account.',
    responses={
        200: {'model': AccountResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_account(af: AccountForm, response: Response):
    account = Account(
        name=af.name,
        description=af.description,
        balance=af.balance,
    )

    try:
        await db.save(account)
        return AccountResponse(
            loc=['create', 'account', 'success'],
            msg='Account created successfully.',
            data=account
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'account', 'error'],
            msg='Can\'t create account now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{aid}',
    description='Update account.',
    responses={
        200: {'model': AccountResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def update_account(aid: ObjectId, uaf: AccountForm, response: Response):
    account = await db.find_one(Account, Account.id == aid)

    if account is not None:
        account.name = uaf.name
        account.description = uaf.description
        account.updated_at = datetime.datetime.utcnow()

        try:
            await db.save(account)
            return AccountResponse(
                loc=['update', 'account', 'success'],
                msg='Account updated successfully.',
                data=account
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'account', 'error'],
                msg='Can\'t update account now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['account', 'not', 'found'],
        msg='Account not found with the provided ID.'
    )


@api.get(
    '/change-status/{aid}',
    description='Change account status.',
    responses={
        200: {'model': AccountResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def change_account_status(aid: ObjectId, response: Response):
    account = await db.find_one(Account, Account.id == aid)

    if account is not None:
        account.status = not account.status

        try:
            await db.save(account)
            return AccountResponse(
                loc=['account', 'status', 'change', 'success'],
                msg='Account status changed successfully.',
                data=account
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['account', 'status', 'change', 'error'],
                msg='Can\'t change account status now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['account', 'not', 'found'],
        msg='Account not found with the provided ID.'
    )


@api.delete(
    '/delete/{aid}',
    description='Delete account.',
    responses={
        200: {'model': AccountResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def delete_account(aid: ObjectId, response: Response):
    account = await db.find_one(Account, Account.id == aid)

    if account is not None:
        try:
            await db.delete(account)
            return AccountResponse(
                loc=['delete', 'account', 'success'],
                msg='Account deleted successfully.'
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'account', 'error'],
                msg='Can\'t delete account now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['account', 'not', 'found'],
        msg='Account not found with the provided ID.'
    )
