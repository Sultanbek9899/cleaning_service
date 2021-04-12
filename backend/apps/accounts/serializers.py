from rest_framework import serializers

from backend.apps.accounts.models import CompanyUser
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

class CustomUserSerializer(RegisterSerializer):

    class Meta:
        model = CompanyUser
        fields = [
            "email",
            "company_name",
            'logo',
            'phone_number',
            'activity_localities',
        ]

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['company_name'] = self.validated_data.get('company_name', '')
        data_dict['logo'] = self.validated_data.get('logo', '')
        data_dict['phone_number'] = self.validated_data.get('phone_number', '')
        data_dict['activity_localities'] = self.validated_data.get('activity_localities', '')
        return data_dict


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + \
            ('company_name', 'logo', 'phone_number', 'activity_localities',)