from fastapi import APIRouter, Response, status, Depends
from odmantic.bson import ObjectId

# Import Models
from models import TransactionType
from models.local_transaction import LocalTransaction

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.auth import Auth

# Import Forms
from models.forms.local_transaction import LocalTransactionForm

# Import Responses
from models.response.local_transaction import \
    LocalTransactionPaginatedResults, \
    LocalTransactionResponse
from models.response.common import ErrorResponse, NotFound

# Import Validators
from validators.form.accountExists import account_exists
from validators.form.clientExists import client_exists

# Import Utils
from datetime import datetime
import pytz

api = APIRouter(
    prefix='/v1/local-transaction',
    tags=["Local Transaction"],
    dependencies=[Depends(Auth().wrapper)]
)


@api.post(
    '/get-paginated',
    description='Get local transaction with or without advanced filters.',
    responses={
        200: {'model': LocalTransactionPaginatedResults}
    }
)
async def get_paginated_local_transaction(pagination: PaginationParameters):
    results = await prepare_result(LocalTransaction, pagination)
    return results


@api.get(
    '/get/{ltid}',
    description='Get Single local transaction.',
    responses={
        200: {'model': LocalTransaction},
        404: {'model': NotFound}
    }
)
async def get_single_local_currency(ltid: ObjectId, response: Response):
    transaction = await db.find_one(LocalTransaction, LocalTransaction.id == ltid)
    if transaction is not None:
        return transaction

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'local', 'transaction'],
        msg='Local Transaction Not Found'
    )


@api.post(
    '/create',
    description='Create local transaction.',
    responses={
        200: {'model': LocalTransactionResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_local_transaction(ltf: LocalTransactionForm, response: Response):
    account = await account_exists(ltf.account)
    client = await client_exists(ltf.client)

    currency = client.currency
    rate = ltf.ad_rate or currency.rate
    amount = rate * ltf.amount
    created_at = ltf.created_at and datetime.strptime(ltf.created_at, '%Y-%m-%dT%H:%M:%S.%fZ') or datetime.utcnow()

    client_balance = 0
    client_ad_balance = 0

    if ltf.type == TransactionType.PAID:
        client_balance = client.balance + ltf.amount
        client_ad_balance = client.ad_balance + amount

    if ltf.type == TransactionType.RECEIVED:
        client_balance = client.balance - ltf.amount
        client_ad_balance = client.ad_balance - amount

    transaction = LocalTransaction(
        amount=ltf.amount,
        client=client,
        type=ltf.type,
        account=account,
        ad_currency=currency,
        ad_rate=rate,
        ad_amount=amount,
        client_balance=client_balance,
        client_ad_balance=client_ad_balance,
        note=ltf.note,
        remark=ltf.remark,
        created_at=created_at
    )

    try:
        await db.save(transaction)
        await transaction.account_next_state()
        await transaction.create_ledger()
        return LocalTransactionResponse(
            loc=['create', 'local', 'transaction', 'success'],
            msg='Local Transaction created successfully.',
            data=transaction
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'local', 'transaction', 'error'],
            msg='Can\'t create local transaction now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{ltid}',
    description='Create local transaction.',
    responses={
        200: {'model': LocalTransactionResponse},
        403: {'model': ErrorResponse}
    }
)
async def update_local_transaction(ltid: ObjectId, ltf: LocalTransactionForm, response: Response):
    transaction = await db.find_one(LocalTransaction, LocalTransaction.id == ltid)
    await transaction.account_prev_state()

    account = await account_exists(ltf.account)
    client = await client_exists(ltf.client)
    currency = client.currency
    rate = ltf.ad_rate or currency.rate
    amount = rate * ltf.amount

    transaction.client = client
    transaction.amount = ltf.amount
    transaction.type = ltf.type
    transaction.account = account
    transaction.note = ltf.note
    transaction.ad_currency = client.currency
    transaction.ad_rate = rate
    transaction.ad_amount = amount
    transaction.remark = ltf.remark
    transaction.updated_at = datetime.utcnow()

    if ltf.type == TransactionType.PAID:
        transaction.client_balance -= ltf.amount
        transaction.client_ad_balance -= amount

    if ltf.type == TransactionType.RECEIVED:
        transaction.client_balance += ltf.amount
        transaction.client_ad_balance += amount

    try:
        await db.save(transaction)
        await transaction.account_next_state()
        await transaction.update_ledger()
        return LocalTransactionResponse(
            loc=['update', 'local', 'transaction', 'success'],
            msg='Local Transaction created successfully.',
            data=transaction
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['update', 'local', 'transaction', 'error'],
            msg='Can\'t create local transaction now, Please try again or contact administrator'
        )


@api.delete(
    '/delete/{ltid}',
    description='Delete local transaction.',
    responses={
        200: {'model': LocalTransactionResponse},
        403: {'model': ErrorResponse}
    }
)
async def delete_local_transaction(ltid: ObjectId, response: Response):
    transaction = await db.find_one(LocalTransaction, LocalTransaction.id == ltid)

    try:
        await transaction.account_prev_state()
        await transaction.delete_ledger()
        await db.delete(transaction)
        return LocalTransactionResponse(
            loc=['delete', 'local', 'transaction', 'success'],
            msg='Local Transaction deleted successfully.'
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['delete', 'local', 'transaction', 'error'],
            msg='Can\'t delete local transaction now, Please try again or contact administrator'
        )
