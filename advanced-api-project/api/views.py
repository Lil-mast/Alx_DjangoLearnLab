from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# Custom filter set for advanced filtering
class BookFilter(FilterSet):
    """
    Custom filter set for Book model with advanced filtering capabilities.
    
    Supports:
    - Exact matching on publication_year and author
    - Case-insensitive contains filtering on title
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

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all Book instances with advanced filtering, searching, and ordering.
    
    Features:
    - Filtering: Filter by publication_year, author, title with various lookup expressions
    - Searching: Full-text search on title and author name fields
    - Ordering: Order by any book field with ascending/descending options
    
    Query Parameter Examples:
    - Filtering: 
        ?publication_year=2020
        ?publication_year__gt=2010&publication_year__lt=2020
        ?author_name=rowling
        ?title=harry
    
    - Searching:
        ?search=potter
    
    - Ordering:
        ?ordering=title (ascending)
        ?ordering=-publication_year (descending)
        ?ordering=author__name,title (multiple fields)
    
    Default permissions: AllowAny (read-only for all users)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Configure filtering, searching, and ordering backends
    filter_backends = [
        DjangoFilterBackend,  # For field-specific filtering
        filters.SearchFilter,  # For full-text search
        filters.OrderingFilter  # For ordering results
    ]
    
    # DjangoFilterBackend configuration
    filterset_class = BookFilter  # Use custom filter set
    # Alternative: filterset_fields = ['publication_year', 'author__name'] for simple filtering
    
    # SearchFilter configuration
    search_fields = [
        'title',           # Exact match search on title
        'author__name',    # Exact match search on author name
        '^title',          # Starts-with search on title
        '^author__name',   # Starts-with search on author name
        '=title',          # Exact match (case-sensitive) on title
        '=author__name',   # Exact match (case-sensitive) on author name
    ]
    
    # OrderingFilter configuration
    ordering_fields = [
        'title',
        'publication_year',
        'author__name',
        'id',
        'created_at'  # If you add this field later
    ]
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Book instance by ID.
    
    Provides read-only access to a specific book.
    No filtering, searching, or ordering needed for single object view.
    
    Default permissions: AllowAny (read-only for all users)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

# ... (Keep the existing Create, Update, Delete views unchanged)

class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all Author instances with basic filtering and search.
    
    Supports:
    - Filtering: Filter by author name
    - Searching: Search by author name
    - Ordering: Order by author name or book count
    
    Query Parameter Examples:
    - Filtering: ?name=rowling
    - Searching: ?search=rowling
    - Ordering: ?ordering=name or ?ordering=-name
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
    """DetailView for retrieving a single Author instance by ID"""
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'