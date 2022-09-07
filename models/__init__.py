from enum import Enum


class TransactionType(str, Enum):
    RECEIVED = 'received'
    PAID = 'paid'


class TransactionReferenceType(str, Enum):
    CLIENT = 'client'
    ACCOUNT = 'account'
