from django.urls import path, include
from DentistBook.dentistsoffice.views import EditDentistsofficeProfileView, DentistsofficeProfileDetailsView, DentistsofficeListView, \
    CreateDentistsofficeServiceView, EditDentistsofficeServiceView, DeleteDentistsofficeServiceView, \
    DentistsofficeServicesDetailsView, EditDentistsofficeWorkingHoursView, DentistsofficeWorkingHoursDetailsView, \
    CreateDentistsofficePictureView, DeleteDentistsofficePictureView, DentistsofficePictureDetailsView

urlpatterns = [
    path('<slug:slug>/edit/', EditDentistsofficeProfileView.as_view(), name='edit-dentistsoffice'),
    path('<slug:slug>/profile/', DentistsofficeProfileDetailsView.as_view(), name='dentistsoffice-details'),
    path('<slug:slug>/service/', include([
        path('create/', CreateDentistsofficeServiceView.as_view(), name='create-service'),
        path('<int:pk>/edit/', EditDentistsofficeServiceView.as_view(), name='edit-service'),
        path('<int:pk>/delete/', DeleteDentistsofficeServiceView.as_view(), name='delete-service'),
        path('<int:pk>/details/', DentistsofficeServicesDetailsView.as_view(), name='service-details'),
    ])),
    path('<slug:slug>/<int:pk>/edit-working-hours/', EditDentistsofficeWorkingHoursView.as_view(), name='edit-working-hours'),
    path('<slug:slug>/<int:pk>/working-hours-details/', DentistsofficeWorkingHoursDetailsView.as_view(), name='working-hours-details'),
    path('<slug:slug>/pictures/', include([
        path('create/', CreateDentistsofficePictureView.as_view(), name='create-picture'),
        path('<int:pk>/delete/', DeleteDentistsofficePictureView.as_view(), name='delete-picture'),
        path('<int:pk>/details/', DentistsofficePictureDetailsView.as_view(), name='picture-details'),
    ])),
    path('all/', DentistsofficeListView.as_view(), name='dentistsoffice-list')
]