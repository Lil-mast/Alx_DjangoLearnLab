from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library, Book

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Function-based view to list all books
def book_list_view(request):
    books = Book.objects.select_related('author').all()
    output = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(output, content_type="text/plain")

# Class-based view to show a library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'  # Optional: we'll create this template
    context_object_name = 'library'