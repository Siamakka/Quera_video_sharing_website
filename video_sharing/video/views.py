from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .serializers import SignUpSerializer
from .serializers import ChangePasswordSerializer
from .serializers import UpdateProfileSerializer
from .serializers import AdminChangePasswordSerializer
from .serializers import AdminUpdateProfileSerializer

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


class UpdateProfileView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        )
    serializer_class = UpdateProfileSerializer
    

class AdminChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAdminUser,
        )
    serializer_class = AdminChangePasswordSerializer


class AdminUpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAdminUser,
        )
    serializer_class = AdminUpdateProfileSerializer