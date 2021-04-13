import hashlib
import uuid
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import generics, permissions, mixins, authentication, status
# Create your views here.
from rest_framework.response import Response

from backend.apps.accounts.serializers import CompanyUserDetailSerializer
from backend.apps.accounts.models import CompanyUser
from .serializers import BookingSerializer


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer


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

    def get_queryset(self):
        locality_pk = self.kwargs.get("locality_pk")
        queryset = CompanyUser.objects.filter(activity_localities__id=locality_pk)\
            .prefetch_related("employees")
