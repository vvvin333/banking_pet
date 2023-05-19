from typing import cast

from django.core.exceptions import BadRequest
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from clients.models import Client


def validate_clients(donor_id: str, recipient_ids: str) -> tuple[Client, QuerySet[Client]]:
    donor: Client = cast(Client, get_object_or_404(Client, personal_tax_number=donor_id))

    try:
        to_ptn = [
            int(ptn)
            for ptn in recipient_ids.replace(" ", "").split(",")
        ]
    except ValueError:
        raise BadRequest("Wrong format")

    recipients = Client.objects.filter(personal_tax_number__in=to_ptn)
    if recipients.count() != len(to_ptn):
        raise BadRequest("Some clients not found")

    return donor, recipients
