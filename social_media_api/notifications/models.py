from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    # Notification types
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'
    MENTION = 'mention'
    SHARE = 'share'
    
    NOTIFICATION_TYPES = [
        (FOLLOW, 'Follow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (MENTION, 'Mention'),
        (SHARE, 'Share'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_received'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_created'
    )
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Generic foreign key for the target object (post, comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor.username} {self.get_verb_display()} - {self.recipient.username}"

    def mark_as_read(self):
        self.read = True
        self.save()

    @classmethod
    def create_notification(cls, recipient, actor, verb, target=None):
        """Helper method to create notifications"""
        notification = cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target
        )
        return notification