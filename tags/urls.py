from django.urls import path
from . import views


urlpatterns = [
    path("", views.ListCreateTagView.as_view()),
]
