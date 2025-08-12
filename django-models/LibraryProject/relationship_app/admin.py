from django.contrib import admin

# Register your models here.
from .models import UserProfile
from .models import Book

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'libraries')
    search_fields = ('title', 'author__name')
    
admin.site.register(Book, BookAdmin)