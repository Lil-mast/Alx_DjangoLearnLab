from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    target_object = serializers.SerializerMethodField()
    verb_display = serializers.CharField(source='get_verb_display', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'actor_username', 'recipient', 'recipient_username',
                 'verb', 'verb_display', 'read', 'timestamp', 'target', 'target_object')
        read_only_fields = ('id', 'timestamp')

    def get_target_object(self, obj):
        if obj.target:
            # You can customize this based on your target models
            if hasattr(obj.target, 'title'):
                return {'id': obj.target.id, 'title': obj.target.title}
            elif hasattr(obj.target, 'content'):
                return {'id': obj.target.id, 'content': obj.target.content[:50]}
        return None