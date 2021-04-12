import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


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