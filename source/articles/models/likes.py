from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import BooleanField, Count, Exists, IntegerField, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from articles.models import BaseModel


class Like(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="Пользователь",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Тип объекта",
    )
    object_id = models.PositiveIntegerField(verbose_name="ID объекта")
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "Like"
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "content_type", "object_id"],
                name="unique_like_per_user_per_object",
            )
        ]

    def __str__(self):
        return f"{self.user} -> {self.content_object}"


def annotate_likes(queryset, user):
    model = queryset.model
    content_type = ContentType.objects.get_for_model(model)
    user_likes = Like.objects.filter(content_type=content_type, object_id=OuterRef("pk"))
    likes_count = user_likes.values("object_id").annotate(count=Count("pk")).values("count")

    if user is not None and user.is_authenticated:
        queryset = queryset.annotate(is_liked=Exists(user_likes.filter(user=user)))
    else:
        queryset = queryset.annotate(is_liked=Value(False, output_field=BooleanField()))

    queryset = queryset.annotate(
        likes_count=Coalesce(Subquery(likes_count, output_field=IntegerField()), 0)
    )
    return queryset
