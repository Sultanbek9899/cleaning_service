from django.urls import path, include, re_path
from django.urls import path, include
from backend.apps.services.views import (
    BookingCreateView,
    CompanyListView,
)
from backend.apps.accounts import views
from backend.apps.services.views import LocalityListView, SelectCompanyView
urlpatterns = [
    path("booking_create/", BookingCreateView.as_view()),
    path("vacant_companies_list/", CompanyListView.as_view()),
    path("add_company_locality/<int:locality_id>/", views.AddCompanyLocalityView.as_view()),
    path("delete_company_locality/<int:locality>/", views.DeleteCompanyLocalityView.as_view()),

    path("localities_list/", LocalityListView.as_view()),
    path("district_localities_list/<int:district_id>/", LocalityListView.as_view()),

    path("select_company/", SelectCompanyView.as_view()),
    path("company_calendar_list/", views.CompanyCalendarView.as_view())
]