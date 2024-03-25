from django.core import validators


def validate_name(name):
    if not name[0].isalpha() or not name[0].isupper():
        raise validators.ValidationError('Name should start with a capital letter!')
    for ch in name:
        if not ch.isalpha():
            raise validators.ValidationError("Name should contain only letters!")


def validate_dentist_picture_file_size(picture_object):
    if picture_object.size > 3145728:
        raise validators.ValidationError("The maximum picture file size that can be uploaded should not exceed 3MB!")