from django.db import models
from django.utils import timezone

from SocialSnap.app_auth.models import User


class Post(models.Model):
    content = models.TextField(max_length=200)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.content


class Profile(models.Model):
    def profile_picture_path(self, filename):
        return f'profile-pictures/{filename}'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True, max_length=200)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_profiles', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_profiles', blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_path, blank=False, null=True)

    def __str__(self):
        return self.user.username
