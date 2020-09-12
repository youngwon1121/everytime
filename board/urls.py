from django.contrib import admin
from django.urls import path
from rest_framework import routers
from .views import BoardViewSet, ArticleViewSet, CommentViewSet, ArticleImageViewSet

router = routers.SimpleRouter()
router.register('board', BoardViewSet)
router.register('article', ArticleViewSet)
router.register('comment', CommentViewSet)
router.register('article_image', ArticleImageViewSet)
urlpatterns = router.urls