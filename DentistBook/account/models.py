from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    MAX_LENGTH_ROLE = 15
    ROLES = (
        ('Client', 'Client'),
        ('Dentistsoffice', 'Dentist'),
    )

    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=ROLES,
        blank=True
    )


