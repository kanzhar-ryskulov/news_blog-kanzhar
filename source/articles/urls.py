from django.urls import path

from articles.views import (
    ArticleDetailView,
    ArticleDeleteView,
    ArticleListView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleLikeView,
    ArticleUnlikeView,
    CommentCreateView,
    CommentLikeView,
    CommentUnlikeView,
)

app_name = "articles"
urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("articles/add/", ArticleCreateView.as_view(), name="create"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path("article/<int:pk>/update/", ArticleUpdateView.as_view(), name="update"),
    path("article/<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete"),
    path("article/<int:pk>/comment-add/", CommentCreateView.as_view(), name="comment-create"),
    path("article/<int:pk>/like/", ArticleLikeView.as_view(), name="article-like"),
    path("article/<int:pk>/unlike/", ArticleUnlikeView.as_view(), name="article-unlike"),
    path("comment/<int:pk>/like/", CommentLikeView.as_view(), name="comment-like"),
    path("comment/<int:pk>/unlike/", CommentUnlikeView.as_view(), name="comment-unlike"),
]
