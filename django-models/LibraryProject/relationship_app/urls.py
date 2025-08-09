from django.urls import path
from .views import book_list_view, LibraryDetailView

urlpatterns = [
    path('', book_list_view, name='book-list'),  # function-based view at root
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),  # class-based view
]
