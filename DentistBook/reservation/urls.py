from django.urls import path, include
from DentistBook.reservation.api_views import ReservationListAPIView
from DentistBook.reservation.views import select_dentistsoffice, select_dentistsoffice_service, select_dentist, select_date, \
    select_time, create_reservation, reservation_success, ReservationsListView, DeleteReservationView, \
    ReservationsExcelDownloadView

urlpatterns = [
    path('create/', include([
        path('select-dentistsoffice/<slug:slug>/', select_dentistsoffice, name='step1-select-dentistsoffice'),
        path('select-dentistsoffice-service/', select_dentistsoffice_service, name='step2-select-dentistsoffice-service'),
        path('select-dentist/', select_dentist, name='step3-select-dentist'),
        path('select-date/', select_date, name='step4-select-date'),
        path('select-time/', select_time, name='step5-select-time'),
        path('confirm-reservation/', create_reservation, name='create-reservation'),
        path('reservation-success/', reservation_success, name='reservation-success')
    ])),
    path('reservations-list/<int:pk>/', ReservationsListView.as_view(), name='reservation-list'),
    path('download-reservations/', ReservationsExcelDownloadView.as_view(), name='download-reservations'),
    path('delete/<int:pk>/', DeleteReservationView.as_view(), name='delete-reservation'),
    path('api/all-reservations/', ReservationListAPIView.as_view(), name='all-reservations-api')
]
