from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_credits(value):
    if value is None or value == '':
        raise ValidationError(
            _('Please enter a valid number of credits'),
            params={'error': value},
        )
