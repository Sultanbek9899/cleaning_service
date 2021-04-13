import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from rest_framework import serializers


class UppercaseValidator(object):

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Ваш пароль должен содержать как минимум 1 заглавную букву, A-Z"),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Пароль должен содержать как минимум 1 заглавную букву, A-Z."
        )


def phone_validator(value):
        if re.search(pattern="[0]{1,1}[0-9]{9,9}$", string=value):
            message = "Пожалуйста проверьте ваш номер. Пример: 0999134494"
            raise serializers.ValidationError(message)
