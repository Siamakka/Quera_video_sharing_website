"""
URL configuration for video_sharing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView

from video.views import SignUpView
from video.views import ChangePasswordView
from video.views import UpdateProfileView
from video.views import AdminChangePasswordView
from video.views import AdminUpdateProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', SignUpView.as_view(), name='auth_signup'),
    path('api/change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('api/update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('api/admin/change_password/<int:pk>/', AdminChangePasswordView.as_view(), name='auth_admin_change_password'),
    path('api/admin/update_profile/<int:pk>/', AdminUpdateProfileView.as_view(), name='admin_update_profile'),
]
