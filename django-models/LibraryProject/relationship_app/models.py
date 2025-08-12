from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 


# Author can write many books (One-to-Many)
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Book belongs to one author
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
# Library holds many books (Many-to-Many)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# One librarian per library (One-to-One)
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    publication_year = models.IntegerField(
        null=True,  # Makes field optional
        blank=True,  # Allows empty in forms
        help_text="Year of publication"
    )
    libraries = models.ManyToManyField('Library')
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        permissions = [
            ("can_add_book", "Can add new book"),
            ("can_change_book", "Can edit existing book"),
            ("can_delete_book", "Can delete book"),
            ("can_view_restricted", "Can view restricted books"),
        ]
        verbose_name = "Book"
        verbose_name_plural = "Books"    