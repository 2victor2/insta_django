from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("users.urls")),
    path("tag/", include("tags.urls")),
    path("post/", include("posts.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
