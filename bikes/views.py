from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Bike
from .serializers import BikeSerializer
from accounts.permissions import IsOwnerUser

# class BikeListAPIView(ListAPIView):
#     serializer_class = BikeSerializer

#     def get_queryset(self):
#         start_date = self.request.query_params.get("start_date")
#         end_date = self.request.query_params.get("end_date")

#         # if no dates selected return empty list
#         if not start_date or not end_date:
#             return []

#         bikes = Bike.objects.all()
#         available_bikes = []

#         for bike in bikes:
#             if bike.is_available_for_dates(start_date, end_date):
#                 available_bikes.append(bike)

#         return available_bikes
from django.db.models import Q
from datetime import datetime
class BikeListAPIView(ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if not start_date or not end_date:
            return Bike.objects.none()

        # ✅ CONVERT STRING → DATE
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        return Bike.objects.filter(
            available_from__lte=start_date,
            available_until__gte=end_date,
        ).exclude(
            bookings__status__in=['pending', 'confirmed'],
            bookings__start_date__lte=end_date,
            bookings__end_date__gte=start_date,
        ).distinct()
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
