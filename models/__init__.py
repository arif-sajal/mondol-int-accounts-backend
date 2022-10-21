from enum import Enum


class TransactionType(str, Enum):
    RECEIVED = 'received'
    PAID = 'paid'
