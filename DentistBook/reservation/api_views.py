from rest_framework import generics as api_views
from DentistBook.reservation.models import Reservation
from DentistBook.reservation.serializers import ReservationListSerializer


class ReservationListAPIView(api_views.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationListSerializer
