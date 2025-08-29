from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'posts/(?P<post_pk>\d+)/comments', views.CommentViewSet, basename='comment')
router.register(r'likes', views.LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    
    # Feed endpoints
    path('feed/', views.user_feed, name='user_feed'),
    path('feed/explore/', views.explore_feed, name='explore_feed'),
    path('feed/personalized/', views.personalized_feed, name='personalized_feed'),
    
    # Like endpoints
    path('user/likes/', views.user_likes, name='user_likes'),
    
    # Post like endpoints
    path('posts/<int:pk>/like/', views.PostViewSet.as_view({'post': 'like'}), name='post_like'),
    path('posts/<int:pk>/likes/', views.PostViewSet.as_view({'get': 'likes'}), name='post_likes'),
]