from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from app_image_upload.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', get_profile),
    path('refresh/', TokenRefreshView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('create-user/', create_user),
    path('get-user-images/', get_user_images),
    path('create-image/', create_image),
    path('get-court', get_court),
    path('create-court', create_court),
    path('set-active-user', set_active_user),
    path('get-active-users', get_active_users),
]
