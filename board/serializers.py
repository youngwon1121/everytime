from rest_framework import serializers
from .models import Board, Article, Comment, ArticleImage

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='writer.username', read_only=True)

    def to_representation(self, instance):
        ret = super(CommentSerializer, self).to_representation(instance)

        if instance.is_anonym:
            ret['username'] = '익명'
        
        return ret

    class Meta:
        model = Comment
        fields = '__all__'

class ArticleImageSerializer(serializers.ModelSerializer):
    photo_thumbnail = serializers.ImageField(read_only=True)
    
    class Meta:
        model = ArticleImage
        fields = ['id', 'photo', 'article', 'photo_thumbnail']

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='writer.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = ArticleImageSerializer(many=True, read_only=True)
    comment_cnt = serializers.IntegerField(read_only=True)
    images_cnt = serializers.IntegerField(read_only=True)
    likes = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        ret = super(ArticleSerializer, self).to_representation(instance)
        
        if instance.is_anonym:
            ret['username'] = '익명'

        return ret


    class Meta:
        model = Article
        fields = ['title', 'username', 'text', 'is_anonym', 'created_at', 'comment_cnt', 'likes', 'images_cnt', 'comments', 'images']