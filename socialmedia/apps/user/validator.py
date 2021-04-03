from django.core.exceptions import ValidationError


def mobile_validator(mobile):
    if mobile[0:2] != '09':
        raise ValidationError('Please follow the mentioned format')


def mobile_length_validator(mobile):
    if len(mobile) != 11:
        raise ValidationError('Please follow the mentioned format:invalid length')
