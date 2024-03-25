from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from DentistBook.dentistsoffice.models import DentistsofficeProfile

UserModel = get_user_model()


class Review(models.Model):
    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]
    MIN_LENGTH_COMMENT = 5
    MAX_LENGTH_COMMENT = 200

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    dentistsoffice = models.ForeignKey(
        DentistsofficeProfile,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
    )
    comment = models.TextField(
        max_length=MAX_LENGTH_COMMENT,
        validators=(validators.MinLengthValidator(MIN_LENGTH_COMMENT),),
        null=True,
        blank=True
    )

    date_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Review by {self.user} for {self.dentistsoffice.name}'
