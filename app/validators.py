from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_credits_length(value):
    if len(value) > 1:
        raise ValidationError(
            _('Credits cannot be more than 9!'),
            params={'value': value},
        )
