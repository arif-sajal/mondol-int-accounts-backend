from fastapi import APIRouter, Response, status
from odmantic.bson import ObjectId

# Import Models
from models.foreign_transaction import ForeignTransaction
from models import TransactionReferenceType

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters

# Import Forms
from models.forms.foreign_transaction import ForeignTransactionForm

# Import Responses
from models.response.foreign_transaction import \
    ForeignTransactionPaginatedResults, \
    ForeignTransactionResponse
from models.response.common import ErrorResponse, NotFound

# Import Validators
from validators.form.clientExists import client_exists
from validators.form.accountExists import account_exists

# Import Utils
from datetime import datetime

api = APIRouter(
    prefix='/v1/foreign-transaction',
    tags=["Foreign Transaction"]
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
    reference = None

    if ftf.reference_type == TransactionReferenceType.CLIENT:
        reference = await client_exists(ftf.reference, loc=['body', 'reference'])
    elif ftf.reference_type == TransactionReferenceType.ACCOUNT:
        reference = await account_exists(ftf.reference, loc=['body', 'reference'])

    transaction = ForeignTransaction(
        from_currency=ftf.from_currency,
        to_currency=ftf.to_currency,
        rate=ftf.rate,
        amount=ftf.amount,
        cv_amount=ftf.amount * ftf.rate,
        type=ftf.type,
        reference_type=ftf.reference_type,
        reference=reference.id,
        note=ftf.note,
        remark=ftf.remark,
        created_at=datetime.utcnow(),
    )

    try:
        await db.save(transaction)
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
async def update_local_transaction(ltid: ObjectId, ftf: ForeignTransactionForm, response: Response):
    transaction = await db.find_one(ForeignTransaction, ForeignTransaction.id == ltid)

    reference = None
    if ftf.reference_type == TransactionReferenceType.CLIENT:
        reference = await client_exists(ftf.reference, loc=['body', 'reference'])
    elif ftf.reference_type == TransactionReferenceType.ACCOUNT:
        reference = await account_exists(ftf.reference, loc=['body', 'reference'])

    transaction.from_currency = ftf.from_currency
    transaction.to_currency = ftf.to_currency
    transaction.rate = ftf.rate
    transaction.amount = ftf.amount
    transaction.cv_amount = ftf.cv_amount
    transaction.type = ftf.type
    transaction.reference_type = ftf.reference_type
    transaction.reference = reference.id
    transaction.note = ftf.note
    transaction.remark = ftf.remark
    transaction.updated_at = datetime.utcnow()

    try:
        await db.save(transaction)
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
