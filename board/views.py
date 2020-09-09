from django.db.models import Count 
from rest_framework import viewsets, mixins
from .serializers import BoardSerializer, ArticleSerializer, CommentSerializer
from .models import Board, Article, Comment
# Create your views here.

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.annotate(comment_cnt=Count('comments'))

class CommentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()