from django.db.models import Count 
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BoardSerializer, ArticleSerializer, CommentSerializer, ArticleImageSerializer
from .models import Board, Article, Comment, ArticleImage
# Create your views here.

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.annotate(comment_cnt=Count('comments', distinct=True), likes=Count('liker', distinct=True), images_cnt=Count('images', distinct=True))

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


class ArticleImageViewSet(viewsets.ViewSet):
    queryset = ArticleImage.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = ArticleImage.objects.all()
        serializer = ArticleImageSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *arg, **kwargs):
        serializer = ArticleImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()   
            return Response({'result': 'success'}, status=status.HTTP_201_CREATED)
        return Response({'result': 'fail'}, status=status.HTTP_400_BAD_REQUEST)