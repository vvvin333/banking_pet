from decimal import Decimal

import pytest
from model_bakery import baker

from clients.models import Client as userClient


@pytest.fixture(scope="function")
def bake_clients():
    def func(count: int, start_amount: Decimal = 100.) -> list[userClient]:
        return [
            baker.make(
                userClient,
                personal_tax_number=i,
                account=start_amount,
            )
            for i in range(count)
        ]

    return func
