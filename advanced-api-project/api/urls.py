from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for optional viewset usage
router = DefaultRouter()
# router.register('books', views.BookViewSet)  # Optional for future expansion

urlpatterns = [
    # Book CRUD endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author endpoints (read-only)
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Include router URLs if using viewsets
    # path('', include(router.urls)),
]

# API root view
urlpatterns += [
    path('', views.BookListView.as_view(), name='api-root'),
]