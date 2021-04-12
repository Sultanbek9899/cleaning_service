from django.contrib import admin

from .models import CompanyUser


@admin.register(CompanyUser)
class PartnerLogosAdmin(admin.ModelAdmin):
    list_display = ['email', "company_name"]
# Register your models here.
