from rest_framework import serializers
from .models import Bike


class BikeSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Bike
        fields = (
            'id',
            'title',
            'price_per_day',
            'owner',
            'available',
        )

    def get_available(self, bike):
        request = self.context.get('request')
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')

        if not start or not end:
            return None  # frontend has not selected dates yet

        return bike.is_available_for_dates(start, end)
