from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    locality = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = Booking
        fields = (
            "email",
            "phone_number",
            "locality",
            "address",
            "date",
            "created",
            "updated",
        )
