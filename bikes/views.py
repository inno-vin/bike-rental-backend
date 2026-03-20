from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils.dateparse import parse_date

from .models import Bike
from .serializers import BikeSerializer
from accounts.permissions import IsOwnerUser


class BikeListAPIView(ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        # ❌ If no dates → return empty
        if not start_date or not end_date:
            return Bike.objects.none()

        # ✅ Convert string → date safely
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        # ❌ If parsing failed
        if not start_date or not end_date:
            return Bike.objects.none()

        # ✅ Get bikes within availability window
        bikes = Bike.objects.filter(
            available_from__isnull=False,
            available_until__isnull=False,
            available_from__lte=start_date,
            available_until__gte=end_date,
        )

        # ✅ Exclude bikes that have overlapping bookings (SAFE way)
        bikes = bikes.exclude(
            Q(bookings__status__in=['pending', 'confirmed']) &
            Q(bookings__start_date__lte=end_date) &
            Q(bookings__end_date__gte=start_date)
        )

        return bikes.distinct()


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