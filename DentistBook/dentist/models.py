from django.core import validators
from django.db import models
from DentistBook.dentist.validators import validate_name, validate_dentist_picture_file_size
from DentistBook.dentistsoffice.models import DentistsofficeProfile


class Dentist(models.Model):
    MIN_LENGTH_NAME = 2
    MAX_LENGTH_NAME = 30
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_NAME),
            validate_name
        ),
        null=False,
        blank=False
    )
    about = models.TextField(
        null=False,
        blank=False
    )
    dentist_picture = models.ImageField(
        upload_to='dentist-profile-pictures',
        validators=(validate_dentist_picture_file_size,),
        null=True,
        blank=True,
    )
    dentistsoffice = models.ForeignKey(
        DentistsofficeProfile,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
