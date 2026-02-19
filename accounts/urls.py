
from django.urls import path
from .views import RegisterAPIView, BecomeOwnerAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('become-owner/', BecomeOwnerAPIView.as_view(), name='become-owner'),
]
