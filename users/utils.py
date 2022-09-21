from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(
        self, name, email, password, private_profile, is_superuser, **extra_fields
    ):

        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            private_profile=private_profile,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, name, email, password, private_profile, **extra_fields):

        return self._create_user(
            name, email, password, private_profile, True, **extra_fields
        )

    def create_user(self, name, email, password, private_profile, **extra_fields):

        return self._create_user(
            name, email, password, private_profile, False, **extra_fields
        )
