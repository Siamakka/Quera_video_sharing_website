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
from django.urls import include
from django.urls import re_path

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import SignUpView
from user.views import ChangePasswordView
from user.views import UpdateProfileView
from user.views import AdminChangePasswordView
from user.views import AdminUpdateProfileView
from user.viewsets import UserViewSet

from video.views import CategoryListCreateView
from video.views import CategoryDetailView
from video.views import VideoListCreateView
from video.views import VideoDetailView
from video.views import CommentDetailView
from video.views import CommentListCreateView
from video.views import VideoDetailWithViewCount
from video.views import LikeVideoView
from video.views import DislikeVideoView
from video.views import AddCommentView
from video.views import VideoCommentsView

from subscription.views import create_payment
from subscription.views import confirm_payment

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from debug_toolbar.toolbar import debug_toolbar_urls




schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename= 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', SignUpView.as_view(), name='auth_signup'),
    path('api/change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('api/update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('api/admin/change_password/<int:pk>/', AdminChangePasswordView.as_view(), name='auth_admin_change_password'),
    path('api/admin/update_profile/<int:pk>/', AdminUpdateProfileView.as_view(), name='admin_update_profile'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('videos/<int:pk>/', VideoDetailWithViewCount.as_view(), name='video-detail'),
    path('videos/<int:video_id>/like/', LikeVideoView.as_view(), name='video-like'),
    path('videos/<int:video_id>/dislike/', DislikeVideoView.as_view(), name='video-dislike'),
    path('videos/<int:video_id>/add_comment/', AddCommentView.as_view(), name='add-comment'),
    path('videos/<int:video_id>/comments/', VideoCommentsView.as_view(), name='video-comments'),

    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

    path('create-payment/<int:plan_id>/', create_payment, name='create_payment'),
    path('confirm-payment/<str:transaction_id>/', confirm_payment, name='confirm_payment'),
] + debug_toolbar_urls()
