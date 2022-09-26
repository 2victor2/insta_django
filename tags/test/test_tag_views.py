from rest_framework.test import APITestCase
from tags.serializers import TagSerializer
from rest_framework.views import status
from users.models import User
from tags.models import Tag


class TestTagView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_name = "Jorginho"
        cls.email = "jorginho_joga_10@gmail.com"
        cls.password = "123456"
        cls.private_profile = False

        cls.user = User.objects.create_user(
            name=cls.user_name,
            email=cls.email,
            password=cls.password,
            private_profile=cls.private_profile,
        )
        cls.name = "Diversão"
        cls.tag = Tag.objects.create(name=cls.name)

    def test_should_create_tag(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post("/tag/", {"name": "Culinária"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["id"])

    def test_should_not_create_tag_with_repeated_name(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.email, "password": self.password}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post("/tag/", {"name": "Diversão"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_create_tag_without_token(self):
        response = self.client.post("/tag/", {"name": "Culinária"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_list_all_tags(self):
        response = self.client.get("/tag/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(TagSerializer(instance=self.tag).data, response.data["results"])

    def test_should_list_all_tags_filtering_by_name(self):
        response = self.client.get("/tag/?name=Diversão")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(TagSerializer(instance=self.tag).data, response.data["results"])
