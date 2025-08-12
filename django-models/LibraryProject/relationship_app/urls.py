from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Import all views from the current app
from .views import list_books, LibraryDetailView
from .views import register_view, login_view, logout_view
from .views import(
    add_book,
   edit_book,
     delete_book,
     list_books,
     LibraryDetailView
)


urlpatterns = [
    # Function-based view URL (Task 4)
    path('books/', list_books, name='list_books'),
    # Class-based view URL (Task 4)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', 
         LoginView.as_view(template_name='relationship_app/login.html'),  # Added
         name='login'),
    path('logout/', 
         LogoutView.as_view(template_name='relationship_app/logout.html'),  # Added
         name='logout'),
    # Book management URLs
    path('books/add/', add_book, name='add_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),

    # Library URLs
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
