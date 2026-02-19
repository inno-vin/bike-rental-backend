from django.urls import path
from .views import (
    BookingCreateAPIView,
    MyBookingsAPIView,
    BookingStatusUpdateAPIView,
    OwnerBookingsAPIView,

)

urlpatterns = [
    path('bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/mine/', MyBookingsAPIView.as_view(), name='my-bookings'),
    path('bookings/<int:pk>/status/', BookingStatusUpdateAPIView.as_view()),
    path('bookings/owner/', OwnerBookingsAPIView.as_view()),


]
