from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

# Function-based view (explicitly showing Book.objects.all() as requested)
def list_books(request):
    # Basic version using all() - exactly as requested
    all_books = Book.objects.all()  # This is now explicitly included
    
    # Optimized version (kept for reference but commented out)
    # books = Book.objects.select_related('author').all()
    
    return render(request, 'relationship_app/list_books.html', {
        'books': all_books  # Using the non-optimized version per request
    })

# Class-based view (unchanged optimized version)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related('books__author')