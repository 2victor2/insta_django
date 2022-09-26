from users.serializers import UserSerializer
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = "Jorginho"
        cls.email = "jorginho_joga_10@gmail.com"
        cls.password = "123456"
        cls.private_profile = False

        cls.user = User.objects.create_user(
            name=cls.name,
            email=cls.email,
            password=cls.password,
            private_profile=cls.private_profile,
        )

    def test_should_create_user(self):
        response = self.client.post(
            "/user/register/",
            {
                "name": "novo_user",
                "email": "novo_user@email.com",
                "password": "12345678",
                "private_profile": False,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["id"])

    def test_create_user_should_not_return_password(self):
        response = self.client.post(
            "/user/register/",
            {
                "name": "novo_user",
                "email": "novo_user2@email.com",
                "password": "12345678",
                "private_profile": False,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(hasattr(response.data, "password"))

    def test_should_login_as_user(self):
        response = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["refresh"])
        self.assertTrue(response.data["access"])

    def test_should_list_all_users(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get("/user/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(UserSerializer(instance=self.user).data, response.data["results"])

    def test_should_list_all_users_filtering_by_name(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get("/user/?name=Jorginho")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(UserSerializer(instance=self.user).data, response.data["results"])

    def test_should_list_user_profile(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get("/user/profile/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["id"], str(self.user.id))

    def test_should_update_user_with_own_token(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response_update = self.client.patch(
            "/user/profile/",
            {"name": "Jorge", "password": "1234"},
        )

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data["name"], "Jorge")
        self.assertFalse(hasattr(response_update.data, "password"))

    def test_should_not_update_without_token(self):
        response_update = self.client.patch(
            "/user/profile/", {"name": "Updated_Username", "password": "1234"}
        )

        self.assertEqual(response_update.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_delete_user_with_own_token(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response_delete = self.client.delete("/user/profile/")

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_not_delete_without_token(self):
        response_delete = self.client.delete("/user/profile/")

        self.assertEqual(response_delete.status_code, status.HTTP_401_UNAUTHORIZED)
