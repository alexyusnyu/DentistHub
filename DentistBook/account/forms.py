from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from DentistBook.account.models import AppUser
from DentistBook.dentistsoffice.models import DentistsofficeProfile
from DentistBook.client.models import ClientProfile
from django import forms

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    role = forms.ChoiceField(
        choices=AppUser.ROLES,
        widget=forms.RadioSelect,
        required=True,
        initial='Client'
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'role')

    def save(self, commit=True):
        user = super().save(commit)
        if user.role == 'Client':
            profile = ClientProfile(
                user=user
            )
        else:
            profile = DentistsofficeProfile(
                user=user
            )
        if commit:
            profile.save()
        return user
