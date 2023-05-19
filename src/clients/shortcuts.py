from decimal import Decimal

from django.core.exceptions import BadRequest

from clients.constants import MONEY_PRECISION
from clients.models import Client


def process_payment(
        donor: Client,
        recipients: list[Client],
        amount: Decimal
) -> list[Client]:
    if donor.account < amount:
        raise BadRequest("Insufficient funds")

    share_payment = round(
        amount / len(recipients),
        MONEY_PRECISION,
    )
    donor.account -= share_payment * len(recipients)
    for recipient in recipients:
        recipient.account += share_payment
    clients = [donor] + recipients
    Client.objects.bulk_update(clients, ["account"])

    return clients
