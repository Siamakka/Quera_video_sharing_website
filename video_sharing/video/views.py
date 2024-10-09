from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import SignUpSerializer
from .serializers import ChangePasswordSerializer

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        AllowAny,
        )
    serializer_class = SignUpSerializer

    
class ChangePasswordView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        )
    serializer_class = ChangePasswordSerializer
    