from functools import wraps
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Book
from .models import Library
from django.views.generic.edit import CreateView


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
    # Authentication Views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

def register_view(request):  # Make sure this exists
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

# Existing Views (with login_required decorator for protected views)
@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related('books__author')
    
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden()
            if not hasattr(request.user, 'profile'):
                return HttpResponseForbidden()
            if request.user.profile.role != role:
                return HttpResponseForbidden()
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
@login_required
@role_required('ADMIN')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@role_required('LIBRARIAN')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@role_required('MEMBER')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')