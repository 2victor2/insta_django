from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from rest_framework import generics
from .models import User


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned users to a given name,
        by filtering agaist a `name` query parameter in the URL.
        """
        queryset = User.objects.all()
        name = self.request.query_params.get("name")

        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(email=self.request.user)
