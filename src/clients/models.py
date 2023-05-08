from django.db import models


class Client(models.Model):
    personal_tax_number = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="Tax number",
    )
    account = models.DecimalField(
        default=0.,
        max_digits=20,
        decimal_places=2,
    )

    def __str__(self) -> str:
        return str(self.personal_tax_number)

    def __repr__(self) -> str:
        return f"Client number: {self.__str__()}"

