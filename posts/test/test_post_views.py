from rest_framework.test import APITestCase, APIRequestFactory
from post_medias.serializers import PostMediaSerializer
from tags.serializers import TagNameSerializer
from posts.serializers import PostSerializer
from post_medias.models import PostMedia
from rest_framework.views import status
from users.models import User
from posts.models import Post
from tags.models import Tag


class TestPostView(APITestCase, APIRequestFactory):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_email = "jorginho_joga_10@gmail.com"
        cls.user_pwd = "123456"
        cls.private_user_email = "igo_senio_oficial@gmail.com"
        cls.user = User.objects.create_user(
            name="Jorginho",
            email=cls.user_email,
            password=cls.user_pwd,
            private_profile=False,
        )
        cls.private_user = User.objects.create_user(
            name="Igo",
            email=cls.private_user_email,
            password=cls.user_pwd,
            private_profile=True,
        )
        cls.tag = Tag.objects.create(name="Diversão")

    def test_should_create_post(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["id"])

    def test_should_not_create_post_without_post_medias_or_tags(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response = self.client.post(
            "/post/",
            {
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_create_post_with_post_medias_or_tags_empty(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(
            "/post/",
            {
                "post_medias": [],
                "description": "fun post",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            "/post/",
            {
                "post_tags": [],
                "description": "fun post",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_create_post_without_token(self):
        media = open("./posts/test/test.jpeg", "rb")
        response = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_list_all_non_private_posts(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_post = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )

        response = self.client.get("/post/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response_post.data, response.data["results"])

    def test_should_not_list_private_posts(self):
        response_login = self.client.post(
            "/user/login/",
            {"email": self.private_user_email, "password": self.user_pwd},
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_post = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        response = self.client.get("/post/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(response_post.data, response.data["results"])
        self.assertEqual(len(response.data["results"]), 0)

    def test_should_list_posts_filtering_by_mimetype(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_post = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        response = self.client.get("/post/?mimetype=JPG")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIn(response_post.data, response.data["results"])

    def test_should_list_posts_filtering_by_tag_name(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_post = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        response = self.client.get("/post/?tag_name=Diversão")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIn(response_post.data, response.data["results"])

    def test_should_list_posts_filtering_by_tag_name(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_post = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        response = self.client.get(
            "/post/?upload_date_after=2022-09-25&upload_date_before=2022-11-25"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIn(response_post.data, response.data["results"])

    def test_should_update_post(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_create = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        post_id = response_create.data["id"]
        update_media = open("./posts/test/update_test.jpg", "rb")
        response_update = self.client.patch(
            f"/post/{post_id}/",
            {
                "post_medias": [update_media],
                "description": "fun post with two medias",
            },
        )

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_update.data["description"], "fun post with two medias"
        )
        self.assertEqual(len(response_update.data["medias"]), 1)

    def test_should_not_update_post_with_post_medias_or_tags_empty(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_create = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        post_id = response_create.data["id"]
        response_update = self.client.patch(
            f"/post/{post_id}/",
            {
                "post_tags": "", # Request factory auto removes the field if it is empty array
                "description": "fun post with two medias",
            },
        )

        self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)

        response_update = self.client.patch(
            f"/post/{post_id}/",
            {
                "post_medias": "",
                "description": "fun post with two medias",
            },
        )

        self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_update_post_without_token(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_create = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        post_id = response_create.data["id"]
        self.client.credentials()
        update_media = open("./posts/test/update_test.jpg", "rb")
        response_update = self.client.patch(
            f"/post/{post_id}/",
            {
                "post_medias": [update_media],
                "description": "fun post with two medias",
            },
        )

        self.assertEqual(response_update.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_update_post_without_being_owner(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_create = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        post_id = response_create.data["id"]
        response_login = self.client.post(
            "/user/login/",
            {"email": self.private_user_email, "password": self.user_pwd},
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        update_media = open("./posts/test/update_test.jpg", "rb")
        response_update = self.client.patch(
            f"/post/{post_id}/",
            {
                "post_medias": [update_media],
                "description": "fun post with two medias",
            },
        )

        self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_delete_post(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_create = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        post_id = response_create.data["id"]
        response_delete = self.client.delete(f"/post/{post_id}/")

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_not_delete_post_without_token(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_create = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        post_id = response_create.data["id"]
        self.client.credentials()
        response_delete = self.client.delete(f"/post/{post_id}/")

        self.assertEqual(response_delete.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_delete_post_without_being_owner(self):
        response_login = self.client.post(
            "/user/login/", {"email": self.user_email, "password": self.user_pwd}
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        media = open("./posts/test/test.jpeg", "rb")
        response_create = self.client.post(
            "/post/",
            {
                "post_medias": media,
                "description": "fun post",
                "post_tags": self.tag.name,
            },
        )
        post_id = response_create.data["id"]
        response_login = self.client.post(
            "/user/login/",
            {"email": self.private_user_email, "password": self.user_pwd},
        )
        token = response_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response_delete = self.client.delete(f"/post/{post_id}/")

        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
