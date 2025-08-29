from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('unread/', views.UnreadNotificationListView.as_view(), name='unread_notifications'),
    path('stats/', views.notification_stats, name='notification_stats'),
    path('<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]