
from django.urls import path
from .views import BikeListAPIView, BikeCreateAPIView, MyBikesAPIView

urlpatterns = [
    path('bikes/', BikeListAPIView.as_view(), name='bike-list'),
    path('bikes/create/', BikeCreateAPIView.as_view(), name='bike-create'),
    path('bikes/mine/', MyBikesAPIView.as_view(), name='my-bikes'),
]
