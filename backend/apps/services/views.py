import hashlib
import uuid
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import (
    generics,
    permissions,
    mixins,
    authentication,
    status,
    serializers,
    exceptions
)
# Create your views here.
from rest_framework.response import Response

from backend.apps.accounts.serializers import CompanyUserDetailSerializer
from backend.apps.accounts.models import CompanyUser, Employee
from .models import Locality, Booking
from .serializers import (
    BookingSerializer,
    CreateBookingSerializer,
    LocalitySerializer, BookingTokenSerializer
)

from rest_framework.views import APIView

from .utils import attach_vacant_employee


class BookingCreateView(generics.CreateAPIView):
    serializer_class = CreateBookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        salt = uuid.uuid4().hex
        token = hashlib.sha256(salt.encode('utf-8')).hexdigest()
        cache.set(instance.id, token, timeout=60)
        data = {
            "instance": serializer.data,
            "booking_token": token
        }
        headers = self.get_success_headers(serializer.data)
        return Response(data=data, status=status.HTTP_201_CREATED, headers=headers)


class CompanyListView(generics.ListAPIView):
    serializer_class = CompanyUserDetailSerializer
    queryset = None

    def get_queryset(self):
        locality_pk = self.kwargs.get("locality_pk")
        queryset = CompanyUser.objects.filter(activity_localities__id=locality_pk)\
            .prefetch_related("employees")
        queryset = queryset.filter(queryset.employyes__work_status == Employee.WORK_STATUS_VACANT)
        return queryset


class LocalityListView(generics.ListAPIView):
    serializer_class = LocalitySerializer

    def get_queryset(self):
        if self.kwargs.get("district_id", None):
            queryset = Locality.objects.filter(district_id=self.kwargs.get("district_id"))
            return queryset
        return Locality.objects.all()


class SelectCompanyView(APIView):

    def post(self, request):
        serializer = BookingTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            booking_id = serializer.data['booking_id']
            comapny_id = serializer.data['company_id']
            if cache.get(key=booking_id, default=None):
                try:
                    booking_instance = Booking.objects.get(id=booking_id)
                    booking_instance.company_id = comapny_id
                    employee = attach_vacant_employee(comapny_id, booking_instance.time)
                    if employee:
                        booking_instance.performer_employee = employee
                        return Response(
                            status=status.HTTP_200_OK,
                            data={"message": "Бронь успешна выполнена"}
                        )
                    else:
                        return Response(status=status.HTTP_404_NOT_FOUND, data={
                            'message': "У данной компании нету свободных сотрудников"})
                except exceptions.NotFound:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={'message': "Бронь не найдена. Пожалуйста убедитесь в том , что вы создали вашу бронь"})
            raise serializers.ValidationError("Уникальный токен не найден. Возможно уникальный токен устарел. Попробуйте ещё раз")