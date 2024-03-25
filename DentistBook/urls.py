from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from DentistBook import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DentistBook.common.urls')),
    path('account/', include('DentistBook.account.urls')),
    path('dentist/', include('DentistBook.dentist.urls')),
    path('dentistsoffice/', include('DentistBook.dentistsoffice.urls')),
    path('client/', include('DentistBook.client.urls')),
    path('reservation/', include('DentistBook.reservation.urls')),
    path('review/', include('DentistBook.review.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'DentistBook Administrator'
admin.site.site_title = 'DentistBook Administrator Page'
admin.site.index_title = 'DentistBook Administrator Page'
