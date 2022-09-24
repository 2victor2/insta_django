from django.db import models
import uuid


class PostMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mimetype = models.CharField(max_length=10)
    thumbnail = models.ImageField(upload_to="thumbnails")
    media = models.FileField(upload_to="post_medias", null=True)
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="medias"
    )
