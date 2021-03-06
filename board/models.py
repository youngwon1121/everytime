from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=30)
    text = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='articles')
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    text = models.TextField()
    is_anonym = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    liker = models.ManyToManyField(User, through='Like', related_name='likes')

    def __str__(self):
        return self.title
    
# 게시판 첨부 이미지
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name='images')
    photo = models.ImageField(upload_to='articles')
    photo_thumbnail = ImageSpecField(source='photo',
                                    processors=[ResizeToFill(480, 480)],
                                    format='JPEG',
                                    options={'quality': 60})

class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article, related_name='comments',on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    text = models.CharField(max_length=200)
    is_anonym = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)