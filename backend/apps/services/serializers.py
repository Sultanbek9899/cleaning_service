from rest_framework import serializers

from backend.apps.accounts.serializers import EmployeeSerializer
from .models import Booking, Locality, District, Region


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = "__all__"
        depth = 1

class LocalitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Locality
        fields = '__all__'
        depth = 2


class DetailBookingSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer()
    performer_employee = EmployeeSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class CreateBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        exclude = [
            "company",
            "performer_employee",
            "created",
            "updated",
        ]


class BookingTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=150)
    company_id = serializers.IntegerField()
    booking_id = serializers.IntegerField()
