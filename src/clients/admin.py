from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("personal_tax_number", "account")
    search_fields = ("personal_tax_number",)
    readonly_fields = ("personal_tax_number", )
