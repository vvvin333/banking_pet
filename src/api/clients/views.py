from django.http import HttpRequest
from ninja import Router

from api.clients import schemas
from clients.models import Client

router = Router(tags=["clients"])


@router.get("/", response=list[schemas.Client])
def get_clients(_: HttpRequest) -> list[Client]:
    return Client.objects.all()
