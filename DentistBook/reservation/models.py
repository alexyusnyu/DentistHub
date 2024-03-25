from django.contrib.auth import get_user_model
from django.core import exceptions
from django.db import models
from DentistBook.dentist.models import Dentist
from DentistBook.dentistsoffice.models import DentistsofficeProfile, DentistsofficeService
from DentistBook.client.models import ClientProfile
from datetime import time

UserModel = get_user_model()


class Reservation(models.Model):

    TIME_SLOT_CHOICES = []
    for hour in range(0, 24):
        for minute in range(0, 60, 30):
            time_slot = time(hour, minute)
            display_text = time_slot.strftime('%H:%M')
            TIME_SLOT_CHOICES.append((time_slot, display_text))

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        DentistsofficeService,
        on_delete=models.CASCADE,
    )

    dentistsoffice = models.ForeignKey(
        DentistsofficeProfile,
        on_delete=models.CASCADE
    )
    dentist = models.ForeignKey(
        Dentist,
        on_delete=models.CASCADE
    )
    date = models.DateField(
        null=False,
        blank=False
    )
    time = models.TimeField(
        choices=TIME_SLOT_CHOICES,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'Reservation for Client: {self.user} Dentist: {self.dentist} at {self.dentistsoffice} on {self.date} {self.time}'

    def save(self, *args, **kwargs):
        existing_reservation = Reservation.objects.filter(
            dentistsoffice=self.dentistsoffice,
            dentist=self.dentist,
            date=self.date,
            time=self.time,
        ).exclude(pk=self.pk).first()

        if existing_reservation:
            raise exceptions.ValidationError("A reservation with the same attributes already exists.")

        super().save(*args, **kwargs)
