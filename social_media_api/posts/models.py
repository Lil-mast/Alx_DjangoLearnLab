from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes_given'
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes_received'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'post']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Post(models.Model):
    # ... existing Post fields ...
    
    @property
    def like_count(self):
        return self.likes_received.count()

    @property
    def is_liked_by_user(self, user):
        if user.is_authenticated:
            return self.likes_received.filter(user=user).exists()
        return False

