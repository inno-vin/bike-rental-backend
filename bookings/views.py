from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import UpdateAPIView
from .serializers import BookingStatusUpdateSerializer
from .permissions import IsBikeOwner

class BookingCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)

class MyBookingsAPIView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user)

class BookingStatusUpdateAPIView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsBikeOwner]


from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OwnerBookingSerializer

class OwnerBookingsAPIView(ListAPIView):
    serializer_class = OwnerBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            bike__owner=self.request.user
        ).order_by('-created_at')
