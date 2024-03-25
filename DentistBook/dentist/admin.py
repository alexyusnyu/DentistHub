from django.contrib import admin
from DentistBook.dentist.models import Dentist


@admin.register(Dentist)
class AdminDentist(admin.ModelAdmin):
    list_display = ['name', 'dentistsoffice']
    list_filter = ['dentistsoffice']
    list_display_links = ['name', 'dentistsoffice']
    list_per_page = 50
    search_fields = ['name', 'dentistsoffice__name']
    search_help_text = 'Search by Dentist Name, dentistsoffice Name'
