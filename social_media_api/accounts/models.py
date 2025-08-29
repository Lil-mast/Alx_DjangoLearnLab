from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        """Return users that this user is following"""
        return self.following_set.count()

    def __str__(self):
        return self.username


    def is_following(self, user):
        """Check if this user is following another user"""
        return self.following_set.filter(id=user.id).exists()

    def add_follower(self, user):
        """Add a follower (user follows this user)"""
        if user != self and not self.followers.filter(id=user.id).exists():
            self.followers.add(user)
            return True
        return False

    def remove_follower(self, user):
        """Remove a follower (user unfollows this user)"""
        if self.followers.filter(id=user.id).exists():
            self.followers.remove(user)
            return True
        return False

    def follow(self, user):
        """Make this user follow another user"""
        if user != self and not user.followers.filter(id=self.id).exists():
            user.followers.add(self)
            return True
        return False

    def unfollow(self, user):
        """Make this user unfollow another user"""
        if user.followers.filter(id=self.id).exists():
            user.followers.remove(self)
            return True
        return False