from django.db.models import Count 
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BoardSerializer, ArticleSerializer, CommentSerializer
from .models import Board, Article, Comment
# Create your views here.

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.annotate(comment_cnt=Count('comments', distinct=True), likes=Count('liker', distinct=True))

    @action(detail=True, methods=['post'])
    def like(self, request, *args, **kwargs):
        article = self.get_object()
        article.liker.add(request.user)
        return Response({'result': 'success'}, status=status.HTTP_201_CREATED)

class CommentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()