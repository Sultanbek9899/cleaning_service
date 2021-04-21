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
    CreateBookingSerializer,
    LocalitySerializer, BookingTokenSerializer, DetailBookingSerializer
)

from rest_framework.views import APIView

from .utils import attach_vacant_employee


class BookingCreateView(generics.CreateAPIView):
    serializer_class = CreateBookingSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        salt = uuid.uuid4().hex
        token = hashlib.sha256(salt.encode('utf-8')).hexdigest()
        cache.set(f"{instance.id}", token, timeout=60)
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


class DistrictListView(generics.ListAPIView):
    serializer_class = LocalitySerializer

    def get_queryset(self):
        if self.kwargs.get("district_id", None):
            queryset = Locality.objects.filter(district_id=self.kwargs.get("district_id"))
            return queryset
        return Locality.objects.all()




class SelectCompanyView(APIView):
    serializer_class = BookingTokenSerializer

    def post(self, request):
        serializer = BookingTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            booking_id = serializer.data['booking_id']
            company_id = serializer.data['company_id']
            if cache.get(f"{booking_id}"):
                try:
                    booking_instance = Booking.objects.get(id=booking_id)
                    booking_instance.company_id = company_id
                    employees = Employee.objects.filter(company_id=company_id)\
                        .exclude(booking__eventcalendar__start_time__lte=booking_instance.time,
                                 booking__eventcalendar__end_time__gte=booking_instance.time, )
                    employee = employees.first()
                    print(employee)
                    booking_instance.performer_employee = employee
                    booking_instance.save()
                    booking_serializer = DetailBookingSerializer(instance=booking_instance)
                    return Response(
                        data=booking_serializer.data,
                        status=status.HTTP_200_OK,
                    )
                    # else:
                    #     return Response(status=status.HTTP_404_NOT_FOUND, data={
                    #         'message': "У данной компании нету свободных сотрудников"})
                except exceptions.NotFound:
                    return Response(status=status.HTTP_404_NOT_FOUND, data={'message': "Бронь не найдена. Пожалуйста убедитесь в том , что вы создали вашу бронь"})
            raise serializers.ValidationError("Уникальный токен не найден. Возможно уникальный токен устарел. Попробуйте ещё раз")




