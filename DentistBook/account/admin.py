from django.contrib import admin
from DentistBook.account.models import AppUser


@admin.register(AppUser)
class AdminAppUser(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'date_joined']
    list_display_links = ['id', 'username', 'email', 'role', 'date_joined']
    list_filter = ['role', 'date_joined']
    list_per_page = 50
    search_fields = ['username', 'email', 'role']
    search_help_text = 'Search by Username, Email, Role'

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.set_password(form.cleaned_data['password'])
        elif form.cleaned_data['password'] != self.model.objects.get(pk=obj.pk).password:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
