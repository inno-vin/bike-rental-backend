# from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import BecomeOwnerSerializer
from .models import Profile


class BecomeOwnerAPIView(UpdateAPIView):
    serializer_class = BecomeOwnerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
