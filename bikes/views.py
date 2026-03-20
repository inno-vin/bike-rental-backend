from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date

from .models import Bike
from .serializers import BikeSerializer
from accounts.permissions import IsOwnerUser
from bookings.models import Booking


class BikeListAPIView(ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if not start_date or not end_date:
            return Bike.objects.none()

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if not start_date or not end_date:
            return Bike.objects.none()

        # ✅ Step 1: bikes in availability range
        bikes = Bike.objects.filter(
            available_from__lte=start_date,
            available_until__gte=end_date,
        )

        # ✅ Step 2: find booked bikes (OVERLAPPING)
        booked_bikes = Booking.objects.filter(
            status__in=['pending', 'confirmed'],
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).values_list('bike_id', flat=True)

        # ✅ Step 3: exclude them safely
        return bikes.exclude(id__in=booked_bikes)


class BikeCreateAPIView(CreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticated, IsOwnerUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyBikesAPIView(ListAPIView):
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bike.objects.filter(owner=self.request.user)