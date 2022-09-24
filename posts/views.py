from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from insta_django.permissions import IsOwner
from .serializers import PostSerializer
from rest_framework import generics
from .models import Post


class ListCreatePostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["tagName", "mimetype", "uploadDateRange"]

    def perform_create(self, serializer):
        owner = self.request.user
        serializer.save(owner=owner)

    def get_queryset(self):
        return self.queryset.filter(owner__private_profile=False).order_by(
            "-created_at"
        )


class UpdateDestroyPostView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsOwner]
    serializer_class = PostSerializer
