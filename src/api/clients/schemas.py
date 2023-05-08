from ninja import Schema


class Client(Schema):
    personal_tax_number: int
    account: float
