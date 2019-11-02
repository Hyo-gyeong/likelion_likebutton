from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Post(models.Model):
   
    title = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()
    name = models.CharField(max_length=20, null=True)
    # 1. 좋아요를 위한 다대다 필드 추가 ( 한 줄이면 충분! 구글링 하면 나옵니다! )
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_user_set', through='Like')

    @property
    def like_count(self):
        return self.like_user_set.count()
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    contents = models.TextField()

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.contents

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
