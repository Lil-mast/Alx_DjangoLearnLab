from django.contrib import admin

# Register your models here.
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['published_date', 'author']
    search_fields = ['title', 'content']
