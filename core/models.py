from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)  # リツイートは空OK
    created_at = models.DateTimeField(auto_now_add=True)

    # 💬 リプライ先
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    # 🔁 リツイート元
    original = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='retweets')

    def is_reply(self):
        return self.parent is not None

    def is_retweet(self):
        return self.original is not None

    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')


