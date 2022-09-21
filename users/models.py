from django.contrib.auth.models import AbstractBaseUser
from .utils import CustomUserManager
from django.db import models
import uuid


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    private_profile = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["name", "private_profile"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()
