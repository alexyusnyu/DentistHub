from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import time
from DentistBook.reservation.models import Reservation


class TimeFilter(admin.SimpleListFilter):
    title = _('Time')
    parameter_name = 'time'

    def lookups(self, request, model_admin):
        return [
            ('morning', _('Morning')),
            ('afternoon', _('Afternoon'))
        ]

    def queryset(self, request, queryset):
        if self.value() == 'morning':
            return queryset.filter(time__lt=time(12, 0))
        if self.value() == 'afternoon':
            return queryset.filter(time__gte=time(12, 0))
        return queryset


@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = ['id', 'date', 'time', 'dentist', 'dentistsoffice', 'user', 'user_email', 'service']
    list_display_links = ['id', 'date', 'time', 'dentist', 'dentistsoffice', 'user', 'user_email', 'service']
    list_filter = ['date', TimeFilter, 'dentist', 'dentistsoffice', 'service']
    list_per_page = 50
    ordering = ['-date', '-time']
    search_fields = ['dentist__name', 'dentistsoffice__name', 'user__username', 'user__email', 'service__service_name']
    search_help_text = 'Search by dentist Name, dentistsoffice Name, Username, Email, Service Name'

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'

