from django.contrib import admin

from .models import CompanyUser, Employee


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ['email', "company_name"]
# Register your models here.


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', "work_status", "age"]