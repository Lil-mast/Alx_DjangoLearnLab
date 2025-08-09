from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-Based View (FBV)
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-Based View (CBV)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'  # Variable name in template
    
    # Optimize database queries
    def get_queryset(self):
        return super().get_queryset().prefetch_related('books__author')