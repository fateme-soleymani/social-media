from django.core.exceptions import ValidationError


def pass_valid(password):
    if len(password) < 5:
        raise ValidationError('Password must be at least 5 characters')
