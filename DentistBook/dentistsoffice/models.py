import uuid
from datetime import time
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from DentistBook.dentistsoffice.validators import validate_dentistsoffice_picture_file_size, \
    validate_dentistsoffice_city_name

UserModel = get_user_model()


class DentistsofficeProfile(models.Model):
    MIN_LENGTH_NAME = 2
    MAX_LENGTH_NAME = 50
    MIN_LENGTH_ADDRESS = 5
    MAX_LENGTH_ADDRESS = 50
    MIN_LENGTH_CITY = 2
    MAX_LENGTH_CITY = 50
    MAX_DIGITS_GEOLOCATION = 18
    DECIMAL_PLACES_GEOLOCATION = 15
    MIN_VALUE_GEOLOCATION_LATITUDE = -90
    MAX_VALUE_GEOLOCATION_LATITUDE = 90
    MIN_VALUE_GEOLOCATION_LONGITUDE = -180
    MAX_VALUE_GEOLOCATION_LONGITUDE = 180
    MIN_LENGTH_ABOUT = 10
    MAX_LENGTH_ABOUT = 500

    class Meta:
        verbose_name = 'Dentists office Profile'

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(validators.MinLengthValidator(MIN_LENGTH_NAME),),
        null=False,
        blank=False
    )
    address = models.CharField(
        max_length=MAX_LENGTH_ADDRESS,
        validators=(validators.MinLengthValidator(MIN_LENGTH_ADDRESS),),
        null=False,
        blank=False
    )
    city = models.CharField(
        max_length=MAX_LENGTH_CITY,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_CITY),
            validate_dentistsoffice_city_name,
        ),
        null=False,
        blank=False
    )
    geolocation_latitude = models.DecimalField(
        max_digits=MAX_DIGITS_GEOLOCATION,
        decimal_places=DECIMAL_PLACES_GEOLOCATION,
        validators=(
            validators.MinValueValidator(MIN_VALUE_GEOLOCATION_LATITUDE),
            validators.MaxValueValidator(MAX_VALUE_GEOLOCATION_LATITUDE)
        ),
        null=True,
        blank=True
        )
    geolocation_longitude = models.DecimalField(
        max_digits=MAX_DIGITS_GEOLOCATION,
        decimal_places=DECIMAL_PLACES_GEOLOCATION,
        validators=(
            validators.MinValueValidator(MIN_VALUE_GEOLOCATION_LONGITUDE),
            validators.MaxValueValidator(MAX_VALUE_GEOLOCATION_LONGITUDE)
        ),
        null=True,
        blank=True
        )
    about = models.TextField(
        max_length=MAX_LENGTH_ABOUT,
        validators=(validators.MinLengthValidator(MIN_LENGTH_ABOUT),),
        null=True,
        blank=True
    )
    dentistsoffice_picture = models.ImageField(
        upload_to='dentistsoffice-profile-pictures',
        validators=(validate_dentistsoffice_picture_file_size,),
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True
    )
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:  # Check if the instance is being added for the first time
            super().save(*args, **kwargs)  # Save the instance to get a valid id
            for day in range(0, 7):
                DentistsofficeWorkingHours.objects.create(
                    dentistsoffice=self,
                    day=day,
                    start_time=None,
                    end_time=None
                )
        if self.name:
            self.slug = slugify(self.name)
        else:
            self.name = slugify(self.user)
            self.slug = slugify(self.user)
        super().save(*args, **kwargs)


class ServiceCategory(models.Model):
    MIN_LENGTH_SERVICE_CATEGORY = 3
    MAX_LENGTH_SERVICE_CATEGORY = 30

    class Meta:
        verbose_name_plural = 'Service Categories'

    category_name = models.CharField(
        max_length=MAX_LENGTH_SERVICE_CATEGORY,
        validators=(validators.MinLengthValidator(MIN_LENGTH_SERVICE_CATEGORY),),
        null=False,
        blank=False
    )

    def __str__(self):
        return self.category_name


class DentistsofficeService(models.Model):
    MIN_LENGTH_DENTISTSOFFICE_SERVICE = 3
    MAX_LENGTH_DENTISTSOFFICE_SERVICE = 50
    MAX_DIGITS_PRICE = 5
    DECIMAL_PLACES_PRICE = 2
    MIN_VALUE_PRICE = 0.01

    class Meta:
        verbose_name_plural = 'Dentists office Services'

    service_name = models.CharField(
        max_length=MAX_LENGTH_DENTISTSOFFICE_SERVICE,
        validators=(validators.MinLengthValidator(MIN_LENGTH_DENTISTSOFFICE_SERVICE),),
        null=False,
        blank=False
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS_PRICE,
        decimal_places=DECIMAL_PLACES_PRICE,
        validators=(validators.MinValueValidator(MIN_VALUE_PRICE),),
        null=False,
        blank=False
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
    )

    dentistsoffice = models.ForeignKey(
        DentistsofficeProfile,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.service_name


class DentistsofficeWorkingHours(models.Model):
    WEEKDAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    TIME_SLOT_CHOICES = []
    for hour in range(0, 24):
        for minute in range(0, 60, 30):
            time_slot = time(hour, minute)
            display_text = time_slot.strftime('%H:%M')
            TIME_SLOT_CHOICES.append((time_slot, display_text))

    dentistsoffice = models.ForeignKey(
        DentistsofficeProfile,
        on_delete=models.CASCADE
    )
    day = models.IntegerField(
        choices=WEEKDAYS,
        null=False,
        blank=False
    )
    start_time = models.TimeField(
        choices=TIME_SLOT_CHOICES,
        null=True,
        blank=True
    )
    end_time = models.TimeField(
        choices=TIME_SLOT_CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('dentistsoffice', 'day')
        verbose_name_plural = 'Dentists office Working Hours'

    def clean(self):
        if self.start_time is not None and self.end_time is not None:
            if self.start_time >= self.end_time:
                raise ValidationError('End time must be later than start time.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


def dentistsoffice_picture_upload_to(instance, filename):
    dentistsoffice_id = instance.dentistsoffice.pk
    upload_filename = f'{uuid.uuid4().hex}.jpg'
    return f'dentistsoffice-pictures/{dentistsoffice_id}/{upload_filename}'


class DentistsofficePicture(models.Model):
    class Meta:
        verbose_name_plural = 'Dentists office Pictures'

    dentistsoffice = models.ForeignKey(
        DentistsofficeProfile,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to=dentistsoffice_picture_upload_to,
        validators=(validate_dentistsoffice_picture_file_size,)
    )

    def __str__(self):
        return f'{self.dentistsoffice.name} - {self.image.name}'