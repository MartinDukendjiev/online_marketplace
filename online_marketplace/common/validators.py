from django.core.exceptions import ValidationError


def image_size_validator_5mb(image_object):
    max_size = 5 * 1024 * 1024

    if image_object.size > max_size:
        raise ValidationError('Image size can not be larger than 5MB')


def validate_phone_number(value):
    if not value.startswith("0") or not value[1:].isdigit() or len(value) != 10:
        raise ValidationError(
            "Invalid phone number. The format should be 0xxxxxxxxx."
        )
