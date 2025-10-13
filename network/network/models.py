from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from rest_framework import serializers

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'poster')
    post_text = models.CharField(max_length = 1000)
    time = models.DateTimeField(default= timezone.now)
    like_counter = models.IntegerField(default=0)


    def __str__(self):
            return f'{self.user}: {self.post_text}'

class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'post_text', 'time', 'is_liked', 'like_counter']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_set.filter(user=request.user).exists()
        return False

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'follower')
    following =  models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'following')
    isFollowing = models.BooleanField(default=True)

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()
    class Meta:
        model = Follow
        fields = '__all__'

class Likes(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE, blank = True, null=True, related_name = 'follower')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'liker')

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
