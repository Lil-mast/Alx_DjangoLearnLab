"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from relationship_app.views import (
    list_books,
    LibraryDetailView,
    register_view,
    login_view,
    logout_view
)
from relationship_app.views import add_book, edit_book, delete_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relationship_app/', include('relationship_app.urls')),
    # Include the bookshelf app URLs if it exists

     # Homepage
    path('', list_books, name='list_books'),
    
    # Library detail
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Auth URLs (better to keep these in relationship_app/urls.py)
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Book management URLs
    path('books/add/', add_book, name='add_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),

    # Library URLs
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'), 
]