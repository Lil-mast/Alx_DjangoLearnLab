from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all Book instances.
    
    Provides read-only access to all books in the database.
    Supports filtering, searching, and ordering.
    
    Default permissions: AllowAny (read-only for all users)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only for all users
    
    # Filtering and searching capabilities
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publication_year', 'author__name']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Book instance by ID.
    
    Provides read-only access to a specific book.
    
    Default permissions: AllowAny (read-only for all users)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only for all users
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new Book instance.
    
    Handles POST requests to create new books with proper validation.
    Includes custom permission requirements.
    
    Permissions: IsAuthenticated - only authenticated users can create books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users
    
    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        Can be used to add additional logic during creation.
        """
        serializer.save()
        # Additional logic can be added here if needed

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing Book instance.
    
    Handles PUT and PATCH requests to update existing books.
    Includes full validation and permission checks.
    
    Permissions: IsAuthenticated - only authenticated users can update books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """
        Custom method called when updating a book instance.
        Can be used to add additional logic during update.
        """
        serializer.save()
        # Additional logic can be added here if needed

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a Book instance.
    
    Handles DELETE requests to remove books from the database.
    Includes permission checks to ensure only authorized users can delete.
    
    Permissions: IsAuthenticated - only authenticated users can delete books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        """
        Custom method called when deleting a book instance.
        Can be used to add additional logic during deletion.
        """
        instance.delete()
        # Additional logic can be added here if needed

# Optional: Author views for completeness
class AuthorListView(generics.ListAPIView):
    """ListView for retrieving all Author instances with their books"""
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """DetailView for retrieving a single Author instance by ID"""
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'