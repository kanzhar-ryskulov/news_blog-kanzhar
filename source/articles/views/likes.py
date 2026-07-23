from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from articles.models import Article, Comment, Like


class LikeToggleBaseView(View):
    model = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Необходима авторизация."}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["pk"])

    def get_likes_count(self, obj, content_type):
        return Like.objects.filter(content_type=content_type, object_id=obj.pk).count()


class LikeAddView(LikeToggleBaseView):
    def _like(self, request, *args, **kwargs):
        obj = self.get_object()
        content_type = ContentType.objects.get_for_model(obj)
        Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj.pk,
        )
        likes_count = self.get_likes_count(obj, content_type)
        return JsonResponse({"liked": True, "likes_count": likes_count})

    def get(self, request, *args, **kwargs):
        return self._like(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._like(request, *args, **kwargs)


class LikeRemoveView(LikeToggleBaseView):
    def _unlike(self, request, *args, **kwargs):
        obj = self.get_object()
        content_type = ContentType.objects.get_for_model(obj)
        Like.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=obj.pk,
        ).delete()
        likes_count = self.get_likes_count(obj, content_type)
        return JsonResponse({"liked": False, "likes_count": likes_count})

    def get(self, request, *args, **kwargs):
        return self._unlike(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self._unlike(request, *args, **kwargs)


class ArticleLikeView(LikeAddView):
    model = Article


class ArticleUnlikeView(LikeRemoveView):
    model = Article


class CommentLikeView(LikeAddView):
    model = Comment


class CommentUnlikeView(LikeRemoveView):
    model = Comment
