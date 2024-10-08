from django.contrib import admin

from accounts.models import (
    FamilyAccount,
    FundRequest,
    SubAccount,
)


@admin.register(SubAccount)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(FundRequest)
class FundRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(FamilyAccount)
class FamilyAccountAdmin(admin.ModelAdmin):
    pass
