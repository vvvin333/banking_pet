from django import forms

from clients.models import Client


class PaymentForm(forms.Form):
    from_ptn = forms.ChoiceField(
        choices=(
            (ptx, ptx)
            for ptx in
            Client.objects.all().values_list("personal_tax_number", flat=True)
        )
    )
    to_ptn = forms.CharField()
    amount = forms.DecimalField(required=True)
