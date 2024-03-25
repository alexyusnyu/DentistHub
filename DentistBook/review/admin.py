from django.contrib import admin
from DentistBook.review.models import Review


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ['user', 'dentistsoffice', 'date_created', 'rating', 'comment']
    list_display_links = ['user', 'dentistsoffice', 'date_created', 'rating', 'comment']
    list_filter = ['dentistsoffice', 'date_created', 'rating']
    list_per_page = 50
    search_fields = ['user__username', 'dentistsoffice__name', 'rating']
    search_help_text = 'Search by Username, Dentists office Name, Rating'
