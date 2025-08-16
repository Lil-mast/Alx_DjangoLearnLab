from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book 
from .models import CustomUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomUser
from .models import UserAdmin
from .models import UserProfile
from django.utils.translation import gettext_lazy as _

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # show these columns in the admin list
    list_filter = ('publication_year', 'author')            # add filters in the right sidebar
    search_fields = ('title', 'author')                     # enable search bar

@admin.register(CustomUser)
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

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'date_of_birth')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'date_of_birth'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
