from django.urls import path
from . import views


urlpatterns = [
    path("", views.ListCreatePostView.as_view()),
    path("<str:pk>/", views.UpdateDestroyPostView.as_view())
]
