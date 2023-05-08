from decimal import Decimal

from ninja import Schema


class Client(Schema):
    personal_tax_number: int
    account: float


class Payment(Schema):
    from_ptn: int
    to_ptn: list[int]
    amount: Decimal
