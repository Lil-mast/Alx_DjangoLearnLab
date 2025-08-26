from rest_framework import generics, permissions
from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter
from django.db.models import Q
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# Custom filter set for advanced filtering
class BookFilter(FilterSet):
    """
    Custom filter set for Book model with advanced filtering capabilities.
    
    Supports:
    - Exact matching on publication_year and author
    - Case-insensitive contains filtering on title and author name
    - Range filtering on publication_year
    """
    publication_year = NumberFilter(field_name='publication_year', lookup_expr='exact')
    publication_year__gt = NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = NumberFilter(field_name='publication_year', lookup_expr='lt')
    publication_year__gte = NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year__lte = NumberFilter(field_name='publication_year', lookup_expr='lte')
    
    author = NumberFilter(field_name='author__id', lookup_expr='exact')
    author_name = CharFilter(field_name='author__name', lookup_expr='icontains')
    
    title = CharFilter(field_name='title', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = [
            'publication_year', 
            'author', 
            'title',
            'publication_year__gt',
            'publication_year__lt',
            'publication_year__gte',
            'publication_year__lte',
            'author_name'
        ]

class BookListView(generics.ListCreateAPIView):
    """
    List and Create view for Book model.
    
    GET: Retrieve all books with filtering, searching, and ordering
    POST: Create a new book (authenticated users only)
    
    Permissions:
    - GET: AllowAny (public read access)
    - POST: IsAuthenticated (only authenticated users can create)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    # Different permissions for different methods
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    # Configure filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', '^title', '^author__name']
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    ordering = ['title']

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, and Delete view for a single Book instance.
    
    GET: Retrieve specific book details
    PUT: Update entire book (authenticated users only)
    PATCH: Partial update of book (authenticated users only)
    DELETE: Remove book (authenticated users only)
    
    Permissions:
    - GET: AllowAny (public read access)
    - PUT/PATCH/DELETE: IsAuthenticated (only authenticated users can modify)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    lookup_field = 'pk'
    
    # Different permissions for different methods
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def perform_update(self, serializer):
        """Custom update logic if needed"""
        serializer.save()
    
    def perform_destroy(self, instance):
        """Custom delete logic if needed"""
        instance.delete()

class BookCreateView(generics.CreateAPIView):
    """
    CreateView specifically for adding new Book instances.
    
    POST: Create a new book (authenticated users only)
    
    Alternative to using ListCreateAPIView if you want separate endpoints
    for listing and creating.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Custom create logic if needed"""
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying existing Book instances.
    
    PUT: Full update of book (authenticated users only)
    PATCH: Partial update of book (authenticated users only)
    
    Alternative to using RetrieveUpdateDestroyAPIView if you want separate endpoints.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """Custom update logic if needed"""
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing Book instances.
    
    DELETE: Remove book from database (authenticated users only)
    
    Alternative to using RetrieveUpdateDestroyAPIView if you want separate endpoints.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        """Custom delete logic if needed"""
        instance.delete()

class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all Author instances with their books.
    
    GET: Retrieve all authors with basic filtering and search
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', '^name', '=name']
    ordering_fields = ['name', 'id']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Author instance with their books.
    
    GET: Retrieve specific author details
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

# Optional: Combined view for all Book operations in one endpoint
class BookViewSet(generics.ViewSet):
    """
    Alternative ViewSet implementation that combines all Book operations.
    
    This provides a more RESTful approach with single endpoint (/books/)
    that handles all HTTP methods appropriately.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def list(self, request):
        """GET /books/ - List all books with filtering"""
        queryset = self.queryset
        queryset = DjangoFilterBackend().filter_queryset(request, queryset, self)
        queryset = filters.SearchFilter().filter_queryset(request, queryset, self)
        queryset = filters.OrderingFilter().filter_queryset(request, queryset, self)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """POST /books/ - Create new book"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """GET /books/{pk}/ - Get specific book"""
        book = generics.get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """PUT /books/{pk}/ - Full update"""
        book = generics.get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        """PATCH /books/{pk}/ - Partial update"""
        book = generics.get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """DELETE /books/{pk}/ - Delete book"""
        book = generics.get_object_or_404(self.queryset, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)