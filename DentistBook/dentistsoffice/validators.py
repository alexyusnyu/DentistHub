from django.core import validators


def validate_dentistsoffice_city_name(city):
    if not city[0].isalpha() or not city[0].isupper():
        raise validators.ValidationError('City name should start with a capital letter!')
    for ch in city:
        if not (ch.isalpha() or ch in "- "):
            raise validators.ValidationError('City name should contain only letters, "-" or spaces!')


def validate_dentistsoffice_picture_file_size(picture_object):
    if picture_object.size > 3145728:
        raise validators.ValidationError("The maximum picture file size that can be uploaded should not exceed 3MB!")