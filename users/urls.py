from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.CreateUserView.as_view()),
    path("profile/", views.UserProfileView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("", views.ListUserView.as_view()),
]
