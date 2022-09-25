from django_filters import FilterSet, CharFilter, DateFromToRangeFilter
from .models import Post


class PostFilter(FilterSet):
    tag_name = CharFilter(field_name="tags__name")
    mimetype = CharFilter(field_name="medias__mimetype")
    upload_date = DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Post
        fields = ["tags__name", "medias__mimetype", "created_at"]
