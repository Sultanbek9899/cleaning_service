from django.urls import path, include, re_path
from django.urls import path, include
from backend.apps.services.views import (
    BookingCreateView,
    CompanyListView

)

urlpatterns = [
    path("booking_create/", BookingCreateView.as_view()),
    path("vacant_companies_list/", CompanyListView.as_view()),
]