from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from .models import Like, Comment

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.user:
        Notification.create_notification(
            recipient=instance.post.author,
            actor=instance.user,
            verb=Notification.LIKE,
            target=instance.post
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.author:
        Notification.create_notification(
            recipient=instance.post.author,
            actor=instance.author,
            verb=Notification.COMMENT,
            target=instance.post
        )