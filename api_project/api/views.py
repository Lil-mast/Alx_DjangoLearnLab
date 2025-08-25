from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    """
    queryset = Book.objects.all()  # Get all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer for serialization

# New ViewSet for complete CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions for Book model.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer