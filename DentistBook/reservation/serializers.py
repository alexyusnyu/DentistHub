from rest_framework import serializers
from DentistBook.reservation.models import Reservation


class ReservationListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')
    dentist_name = serializers.CharField(source='dentist.name')
    dentistsoffice_name = serializers.CharField(source='dentistsoffice.name')
    service_name = serializers.CharField(source='service.service_name')

    class Meta:
        model = Reservation
        fields = ['id', 'user_name', 'dentist_name', 'dentistsoffice_name', 'service_name', 'date', 'time']