from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library

# Function-based view to list all books
def book_list_view(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'book_list.html', {'books': books})

# Class-based view to show library details and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
