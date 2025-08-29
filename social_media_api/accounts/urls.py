from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    
    # Follow management endpoints
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),
    path('followers/', views.get_followers, name='my_followers'),
    path('followers/<int:user_id>/', views.get_followers, name='user_followers'),
    path('following/', views.get_following, name='my_following'),
    path('following/<int:user_id>/', views.get_following, name='user_following'),
    path('follow-status/<int:user_id>/', views.check_follow_status, name='follow_status'),
    
    # GenericAPIView endpoints
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/search/', views.UserSearchView.as_view(), name='user_search'),
]