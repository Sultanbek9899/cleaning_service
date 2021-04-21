from django.contrib import admin

from .models import CompanyUser, Employee, EventCalendar


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ["id", 'email', "company_name"]
# Register your models here.

@admin.register(EventCalendar)
class EventCalendarAdmin(admin.ModelAdmin):
    list_display = ['employee', "booking", 'start_time', 'end_time']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', "work_status", "age"]