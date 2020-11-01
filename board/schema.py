import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.debug import DjangoDebug

from django.contrib.auth.models import User
from .models import Board, Article


class BoardType(DjangoObjectType):

    class Meta:
        model = Board
        fields = '__all__'


class ArticleType(DjangoObjectType):
    writer_name = graphene.String()

    class Meta:
        model = Article
        fields = '__all__'

    def resolve_writer_name(root, info, **kwargs):
        return '익명' if root.is_anonym else root.writer.username

    def resolve_writer(root, info, **kwargs):
        root.writer.is_anonym = root.is_anonym
        return root.writer
            

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

    def resolve_username(root, info, **kwargs):
        return '익명' if root.is_anonym else root.username

class Query(graphene.ObjectType):
    boards = graphene.List(BoardType)
    articles = DjangoListField(ArticleType, id=graphene.Int(), title=graphene.String())
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_boards(root, info, **kwargs):
        return Board.objects.all()
    
    def resolve_articles(root, info, **kwargs):
        return Article.objects.filter(**kwargs).select_related('writer')
    
schema = graphene.Schema(Query)