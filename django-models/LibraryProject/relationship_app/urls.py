from django.urls import path
from .views import book_list_view, LibraryDetailView
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('book-list')),  # 👈 this line redirects root to /books/
    path('books/', book_list_view, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
