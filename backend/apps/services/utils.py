from backend.apps.accounts.models import Employee
from django.db.models import Q

import datetime


def attach_vacant_employee(company_id, time):
    employees = Employee.objects.filter(company_id=company_id)\
                                        .exclude(booking__eventcalendar__start_time__lte=time,
                                                 booking__eventcalendar__end_time__gte=time,)
    if employees:
        return employees.first()
    return None
