from django.urls import path
from .views import list_books, LibraryDetailView
from .views import register_view, login_view, logout_view

urlpatterns = [
    # Function-based view URL (Task 4)
    path('books/', list_books, name='list_books'),
    # Class-based view URL (Task 4)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]