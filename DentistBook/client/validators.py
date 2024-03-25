from django.core import validators


def validate_client_name(name):
    if not name[0].isalpha() or not name[0].isupper():
        raise validators.ValidationError('Name should start with a capital letter!')
    for ch in name:
        if not ch.isalpha():
            raise validators.ValidationError("Name should contain only letters!")


def validate_client_city_name(city):
    if not city[0].isalpha() or not city[0].isupper():
        raise validators.ValidationError('City name should start with a capital letter!')
    for ch in city:
        if not (ch.isalpha() or ch in "- "):
            raise validators.ValidationError('City name should contain only letters, "-" or spaces!')


def validate_client_phone_number(phone_number):
    if phone_number[0] != "0":
        raise validators.ValidationError('Phone number should start with "0"')
    for ch in phone_number:
        if not ch.isdigit():
            raise validators.ValidationError('Phone number should contain only numbers')


def validate_client_picture_file_size(picture_object):
    if picture_object.size > 10485760:
        raise validators.ValidationError("The maximum picture file size that can be uploaded should not exceed 10MB!")