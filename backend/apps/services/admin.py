from django.contrib import admin


from .models import Booking
# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['company', "performer_employee", 'email', 'locality', 'address', 'time']