from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        AllowAny,
        )
    serializer_class = RegistrationSerializer