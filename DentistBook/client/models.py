from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from DentistBook.client.validators import validate_client_name, validate_client_city_name, \
    validate_client_phone_number, validate_client_picture_file_size

UserModel = get_user_model()


class ClientProfile(models.Model):
    MIN_LENGTH_FIRST_NAME = 2
    MAX_LENGTH_FIRST_NAME = 30
    MIN_LENGTH_LAST_NAME = 2
    MAX_LENGTH_LAST_NAME = 50
    MIN_LENGTH_CITY = 2
    MAX_LENGTH_CITY = 50
    MIN_LENGTH_PHONE_NUMBER = 8
    MAX_LENGTH_PHONE_NUMBER = 12

    first_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_FIRST_NAME),
            validate_client_name,
        ),
        null=False,
        blank=False
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_LAST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_LAST_NAME),
            validate_client_name,
        ),
        null=False,
        blank=False
    )
    city = models.CharField(
        max_length=MAX_LENGTH_CITY,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_CITY),
            validate_client_city_name,
        ),
        null=False,
        blank=False
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE_NUMBER,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_PHONE_NUMBER),
            validate_client_phone_number,
        ),
        null=False,
        blank=False
    )

    profile_picture = models.ImageField(
        upload_to='client-profile-pictures',
        validators=(validate_client_picture_file_size,),
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
