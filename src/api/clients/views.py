from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from ninja import Router, Form

from api.clients import schemas
from clients.shortcuts import process_payment
from clients.validators import validate_clients
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
    donor, recipients = validate_clients(payload.from_ptn, payload.to_ptn)

    return process_payment(donor, list(recipients), payload.amount)


@router.get("/transact")
def get_pay_from_client_form(request: HttpRequest) -> HttpResponse:
    form = PaymentForm()
    return render(request, "payment_form.html", {"form": form})
