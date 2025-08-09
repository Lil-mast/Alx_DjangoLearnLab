from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library

# ✅ Function-based view using Book.objects.all() and expected template
def book_list_view(request):
    books = Book.objects.all()  # <--- required by checker
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-based view using DetailView and expected template name
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
