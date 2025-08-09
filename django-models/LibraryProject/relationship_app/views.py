from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view (Task 1)
def list_books(request):
    books = Book.objects.select_related('author').all()  # Optimized query
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view (Tasks 2 & 3)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        # Optimized query with prefetch_related (Task 3)
        return super().get_queryset().prefetch_related('books__author')