from rest_framework import generics
from users.serializers import UserSerializer
from .models import User


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
