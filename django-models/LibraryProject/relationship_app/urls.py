from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Handles /relationship_app/books/
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # No need for separate root view since we're redirecting directly to books
]