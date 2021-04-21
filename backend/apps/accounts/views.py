from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, mixins, authentication, status
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from backend.apps.services.models import Locality
from .models import CompanyUser
from .serializers import CompanyUserDetailSerializer
from backend.apps.services.serializers import DetailBookingSerializer
from backend.apps.services.models import Booking


class AddCompanyLocalityView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]

    def get(self, request):
        locality_id = self.kwargs.get("locality_pk")
        company_user = self.request.user
        company_user.activity_localities.add(locality_id)
        company_user.save()
        serializer = CompanyUserDetailSerializer(company_user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class DeleteCompanyLocalityView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]

    def get(self, request):
        locality_id = self.kwargs.get("locality_pk")
        company_user = self.request.user
        try:
            locality = Locality.objects.get(id=locality_id)
            company_user.activity_localities.remove(locality)
        except ObjectDoesNotExist:
            raise NotFound
        company_user.save()
        serializer = CompanyUserDetailSerializer(company_user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CompanyCalendarView(generics.ListAPIView):
    serializer_class = DetailBookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]

    def get_queryset(self):
        company = self.request.user
        queryset = Booking.objects.filter(company=company).order_by("-time")
        return queryset
