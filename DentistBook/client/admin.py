from django.contrib import admin
from DentistBook.client.models import ClientProfile


@admin.register(ClientProfile)
class AdminClientProfile(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'city', 'phone', 'user']
    list_display_links = ['first_name', 'last_name', 'city', 'phone', 'user']
    list_filter = ['city']
    list_per_page = 50
    search_fields = ['first_name', 'last_name', 'city', 'phone', 'user__username']
    search_help_text = 'Search by First Name, Last Name, City, Phone, Username'
