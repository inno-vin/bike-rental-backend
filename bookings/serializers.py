from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'id',
            'bike',
            'start_date',
            'end_date',
            'status',
        )
        read_only_fields = ('status',)





class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('status',)

    def validate_status(self, value):
        if value not in ['confirmed', 'cancelled']:
            raise serializers.ValidationError(
                "Only confirmed or cancelled is allowed."
            )
        return value


from rest_framework import serializers
from .models import Booking

class OwnerBookingSerializer(serializers.ModelSerializer):
    bike = serializers.CharField(source='bike.title')
    renter = serializers.CharField(source='renter.username')

    class Meta:
        model = Booking
        fields = [
            'id',
            'bike',
            'renter',
            'start_date',
            'end_date',
            'status'
        ]
