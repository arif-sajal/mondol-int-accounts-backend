from fastapi import APIRouter, Response, status, Depends
from odmantic.bson import ObjectId
from settings import settings

# Import Models
from models import TransactionType
from models.foreign_transaction import ForeignTransaction
from models.currency import Currency

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.auth import Auth

# Import Forms
from models.forms.foreign_transaction import ForeignTransactionForm

# Import Responses
from models.response.foreign_transaction import \
    ForeignTransactionPaginatedResults, \
    ForeignTransactionResponse
from models.response.common import ErrorResponse, NotFound

# Import Validators
from validators.form.clientExists import client_exists
from validators.form.currencyExists import currency_exists

# Import Utils
from datetime import datetime

api = APIRouter(
    prefix='/v1/foreign-transaction',
    tags=["Foreign Transaction"],
    dependencies=[Depends(Auth().wrapper)]
)


@api.post(
    '/get-paginated',
    description='Get foreign transaction with or without advanced filters.',
    responses={
        200: {'model': ForeignTransactionPaginatedResults}
    }
)
async def get_paginated_foreign_transaction(pagination: PaginationParameters):
    results = await prepare_result(ForeignTransaction, pagination)
    return results


@api.get(
    '/get/{ltid}',
    description='Get Single foreign transaction.',
    responses={
        200: {'model': ForeignTransaction},
        404: {'model': NotFound}
    }
)
async def get_single_foreign_currency(ltid: ObjectId, response: Response):
    transaction = await db.find_one(ForeignTransaction, ForeignTransaction.id == ltid)
    if transaction is not None:
        return transaction

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'foreign', 'transaction'],
        msg='Local Transaction Not Found'
    )


@api.post(
    '/create',
    description='Create foreign transaction.',
    responses={
        200: {'model': ForeignTransactionResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_foreign_transaction(ftf: ForeignTransactionForm, response: Response):
    client = await client_exists(ftf.client)
    from_currency = await currency_exists(ftf.from_currency)
    to_currency = await db.find_one(Currency, Currency.code == settings.LOCAL_CURRENCY)

    rate = round(ftf.rate, 3)
    amount = round(ftf.amount, 3)
    cv_amount = round(ftf.amount * rate, 3)
    created_at = ftf.created_at and datetime.strptime(ftf.created_at, '%Y-%m-%dT%H:%M:%S.%fZ') or datetime.utcnow()

    if client.currency.id != to_currency.id:
        ad_currency = client.currency
        ad_rate = ftf.ad_rate or round(ad_currency.rate / to_currency.rate, 3)
        ad_cv_amount = round(cv_amount * ad_rate, 3)
    else:
        ad_currency = to_currency
        ad_rate = 1.00
        ad_cv_amount = cv_amount

    client_balance = 0
    client_ad_balance = 0

    if ftf.type == TransactionType.PAID:
        client_balance = client.balance + cv_amount
        client_ad_balance = client.ad_balance + ad_cv_amount

    if ftf.type == TransactionType.RECEIVED:
        client_balance = client.balance - cv_amount
        client_ad_balance = client.ad_balance - ad_cv_amount

    transaction = ForeignTransaction(
        from_currency=from_currency,
        to_currency=to_currency,
        rate=rate,
        amount=amount,
        cv_amount=cv_amount,
        type=ftf.type,
        client=client,
        ad_currency=ad_currency,
        ad_rate=ad_rate,
        ad_cv_amount=ad_cv_amount,
        client_balance=client_balance,
        client_ad_balance=client_ad_balance,
        note=ftf.note,
        remark=ftf.remark,
        created_at=created_at
    )

    try:
        await db.save(transaction)
        await transaction.create_ledger()
        return ForeignTransactionResponse(
            loc=['create', 'foreign', 'transaction', 'success'],
            msg='Foreign Transaction created successfully.',
            data=transaction
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'foreign', 'transaction', 'error'],
            msg='Can\'t create foreign transaction now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{ltid}',
    description='Create foreign transaction.',
    responses={
        200: {'model': ForeignTransactionResponse},
        403: {'model': ErrorResponse}
    }
)
async def update_foreign_transaction(ltid: ObjectId, ftf: ForeignTransactionForm, response: Response):
    transaction = await db.find_one(ForeignTransaction, ForeignTransaction.id == ltid)
    client = await client_exists(ftf.client)
    from_currency = await currency_exists(ftf.from_currency)
    to_currency = await db.find_one(Currency, Currency.code == settings.LOCAL_CURRENCY)

    rate = round(ftf.rate, 3)
    amount = round(ftf.amount, 3)
    cv_amount = round(ftf.amount * rate, 3)

    if client.currency.id != to_currency.id:
        ad_currency = client.currency
        ad_rate = round(ad_currency.rate / to_currency.rate, 3)
        ad_cv_amount = round(cv_amount * ad_rate, 3)
    else:
        ad_currency = to_currency
        ad_rate = 1.00
        ad_cv_amount = cv_amount

    if ftf.type == TransactionType.PAID:
        transaction.client_balance = client.balance + cv_amount
        transaction.client_ad_balance = client.ad_balance + ad_cv_amount

    if ftf.type == TransactionType.RECEIVED:
        transaction.client_balance = client.balance - cv_amount
        transaction.client_ad_balance = client.ad_balance - ad_cv_amount

    transaction.from_currency = from_currency
    transaction.to_currency = to_currency
    transaction.rate = rate
    transaction.amount = amount
    transaction.cv_amount = cv_amount
    transaction.type = ftf.type
    transaction.client = client
    transaction.ad_currency = ad_currency
    transaction.ad_rate = ad_rate
    transaction.ad_cv_amount = ad_cv_amount
    transaction.note = ftf.note
    transaction.remark = ftf.remark
    transaction.updated_at = datetime.now()

    try:
        await db.save(transaction)
        await transaction.update_ledger()
        return ForeignTransactionResponse(
            loc=['update', 'foreign', 'transaction', 'success'],
            msg='Foreign Transaction created successfully.',
            data=transaction
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['update', 'foreign', 'transaction', 'error'],
            msg='Can\'t create foreign transaction now, Please try again or contact administrator'
        )


@api.delete(
    '/delete/{ltid}',
    description='Delete local transaction.',
    responses={
        200: {'model': ForeignTransactionResponse},
        403: {'model': ErrorResponse}
    }
)
async def delete_local_transaction(ltid: ObjectId, response: Response):
    transaction = await db.find_one(ForeignTransaction, ForeignTransaction.id == ltid)

    try:
        await transaction.delete_ledger()
        await db.delete(transaction)
        return ForeignTransactionResponse(
            loc=['delete', 'foreign', 'transaction', 'success'],
            msg='Local Transaction deleted successfully.'
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['delete', 'foreign', 'transaction', 'error'],
            msg='Can\'t delete foreign transaction now, Please try again or contact administrator'
        )
