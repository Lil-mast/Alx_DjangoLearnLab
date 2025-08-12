from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Import all views from the current app
from .views import list_books, LibraryDetailView
from .views import register_view, login_view, logout_view

urlpatterns = [
    # Function-based view URL (Task 4)
    path('books/', list_books, name='list_books'),
    # Class-based view URL (Task 4)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # Authentication URLs
   path('register/', views.register_view, name='register'),
    path('login/', 
         LoginView.as_view(template_name='relationship_app/login.html'),  # Added
         name='login'),
    path('logout/', 
         LogoutView.as_view(template_name='relationship_app/logout.html'),  # Added
         name='logout')
]