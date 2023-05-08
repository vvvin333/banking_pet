from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from ninja import Router, Form

from api.clients import schemas
from clients.constants import MONEY_PRECISION
from clients.forms import PaymentForm
from clients.models import Client

router = Router(tags=["clients"])


@router.get("/", response=list[schemas.Client])
def get_clients(_: HttpRequest) -> list[Client]:
    return Client.objects.all()


@router.post("/transact", response=list[schemas.Client])
def pay_from_client(
    _: HttpRequest, payload: schemas.Payment = Form(...)
) -> list[Client]:
    donor = get_object_or_404(Client, personal_tax_number=payload.from_ptn)
    if donor.account < payload.amount:
        raise BadRequest("Insufficient funds")

    try:
        to_ptn = [
            int(ptn)
            for ptn in payload.to_ptn.split(",")
        ]
    except ValueError:
        raise BadRequest("Wrong format")

    recipients = Client.objects.filter(personal_tax_number__in=to_ptn)
    if recipients.count() != len(to_ptn):
        raise BadRequest("Some clients not found")

    share_payment = round(
        payload.amount/len(to_ptn),
        MONEY_PRECISION,
    )
    donor.account -= share_payment * len(to_ptn)
    for recipient in recipients:
        recipient.account += share_payment
    clients = [donor] + list(recipients)
    Client.objects.bulk_update(clients, ["account"])

    return clients


@router.get("/transact")
def get_pay_from_client_form(request: HttpRequest) -> HttpResponse:
    form = PaymentForm()
    return render(request, "payment_form.html", {"form": form})
