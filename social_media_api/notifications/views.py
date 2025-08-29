from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from django.db.models import Q

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, read=False)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    return Response({'message': 'Notification marked as read'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    notifications = Notification.objects.filter(recipient=request.user, read=False)
    notifications.update(read=True)
    return Response({'message': f'Marked {notifications.count()} notifications as read'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    total = Notification.objects.filter(recipient=request.user).count()
    unread = Notification.objects.filter(recipient=request.user, read=False).count()
    
    return Response({
        'total_notifications': total,
        'unread_notifications': unread,
        'read_notifications': total - unread
    })