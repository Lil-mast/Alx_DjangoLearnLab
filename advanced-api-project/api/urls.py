from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSet usage (optional)
router = DefaultRouter()
router.register(r'books-viewset', views.BookViewSet, basename='book')

urlpatterns = [
    # Traditional CRUD endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # ViewSet endpoints (optional alternative)
    path('', include(router.urls)),
    
    # API root
    path('', views.BookListView.as_view(), name='api-root'),
]