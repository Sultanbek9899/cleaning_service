from allauth.account.adapter import get_adapter
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from backend.apps.accounts.models import CompanyUser
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .validators import phone_validator




class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CompanyUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(
        max_length=10,
        min_length=10,
        required=True,

    )

    class Meta:
        model = CompanyUser
        fields = ('email', 'password', 'password2', "company_name", "phone_number")
        extra_kwargs = {
            'company_name': {'required': True},
        }

    def save(self, request, **kwargs):
        user = super().save(**kwargs)
        user.gender = self.data.get('company_name')
        user.phone_number = self.data.get('phone_number')
        user.save()
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        user = CompanyUser.objects.create(
            email=validated_data['email'],
            company_name=validated_data['company_name'],
            phone_number=validated_data['phone_number']

        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class CompanyUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = [
            "email",
            "company_name",
            "logo",
            "phone_number",
            "activity_localities"
        ]