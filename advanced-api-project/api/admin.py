from django.contrib import admin

# Register your models here.
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publication_year', 'author']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    list_per_page = 20