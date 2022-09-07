from fastapi import APIRouter, Response, status
from odmantic.bson import ObjectId

# Import Models
from models.local_transaction import LocalTransaction
from models import TransactionReferenceType

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters

# Import Forms
from models.forms.local_transaction import LocalTransactionForm

# Import Responses
from models.response.local_transaction import \
    LocalTransactionPaginatedResults, \
    LocalTransactionResponse
from models.response.common import ErrorResponse, NotFound

# Import Validators
from validators.form.clientExists import client_exists
from validators.form.accountExists import account_exists

# Import Utils
from datetime import datetime

api = APIRouter(
    prefix='/v1/local-transaction',
    tags=["Local Transaction"]
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
    reference = None

    if ltf.reference_type == TransactionReferenceType.CLIENT:
        reference = await client_exists(ltf.reference, loc=['body', 'reference'])
    elif ltf.reference_type == TransactionReferenceType.ACCOUNT:
        reference = await account_exists(ltf.reference, loc=['body', 'reference'])

    transaction = LocalTransaction(
        amount=ltf.amount,
        type=ltf.type,
        reference_type=ltf.reference_type,
        reference=reference.id,
        note=ltf.note,
        remark=ltf.remark,
        created_at=datetime.utcnow(),
    )

    try:
        await db.save(transaction)
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

    reference = None
    if ltf.reference_type == TransactionReferenceType.CLIENT:
        reference = await client_exists(ltf.reference, loc=['body', 'reference'])
    elif ltf.reference_type == TransactionReferenceType.ACCOUNT:
        reference = await account_exists(ltf.reference, loc=['body', 'reference'])

    transaction.amount = ltf.amount
    transaction.type = ltf.type
    transaction.reference_type = ltf.reference_type
    transaction.reference = reference.id
    transaction.note = ltf.note
    transaction.remark = ltf.remark
    transaction.updated_at = datetime.utcnow()

    try:
        await db.save(transaction)
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
