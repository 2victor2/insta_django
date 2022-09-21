from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import TagSerializer
from rest_framework import generics
from .models import Tag


class ListCreateTagView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned tags to a given tag name,
        by filtering agaist a `name` query parameter in the URL.
        """
        queryset = Tag.objects.all()
        name = self.request.query_params.get("name")

        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset
