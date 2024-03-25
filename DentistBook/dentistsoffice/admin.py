from django.contrib import admin
from DentistBook.dentistsoffice.models import DentistsofficeProfile, ServiceCategory, DentistsofficeService, DentistsofficeWorkingHours, \
    DentistsofficePicture


@admin.register(DentistsofficeProfile)
class AdminDentistsofficeProfile(admin.ModelAdmin):
    list_display = ['name', 'city', 'address', 'user']
    list_display_links = ['name', 'city', 'address', 'user']
    list_filter = ['city']
    list_per_page = 50
    search_fields = ['name', 'city', 'user__username']
    search_help_text = 'Search by Dentists office Name, City, Username'


@admin.register(ServiceCategory)
class AdminServiceCategory(admin.ModelAdmin):
    list_display = ['category_name']


@admin.register(DentistsofficeService)
class AdminDentistsofficeService(admin.ModelAdmin):
    list_display = ['dentistsoffice', 'category', 'service_name', 'price']
    list_display_links = ['dentistsoffice', 'category', 'service_name', 'price']
    list_filter = (
        ('dentistsoffice', admin.RelatedFieldListFilter),
        ('category', admin.RelatedFieldListFilter),
        'price',
    )
    search_fields = ['dentistsoffice__name', 'service_name', 'category__category_name', 'price']
    search_help_text = 'Search by Dentists office Name, Service Name, Category Name, Price'


@admin.register(DentistsofficeWorkingHours)
class AdminDentistsofficeWorkingHours(admin.ModelAdmin):
    list_display = ['dentistsoffice', 'day', 'start_time', 'end_time']
    list_display_links = ['dentistsoffice', 'day', 'start_time', 'end_time']
    list_filter = ['dentistsoffice', 'day']
    list_per_page = 56
    search_fields = ['dentistsoffice__name']
    search_help_text = 'Search by Dentists office Name'


@admin.register(DentistsofficePicture)
class DentistsofficePictureAdmin(admin.ModelAdmin):
    list_display = ['dentistsoffice', 'image']
    list_display_links = ['dentistsoffice', 'image']
    list_filter = ['dentistsoffice']
    list_per_page = 50
    ordering = ['dentistsoffice']
    search_fields = ['dentistsoffice__name', 'image']
    search_help_text = 'Search by Dentists office Name, Image Name'


