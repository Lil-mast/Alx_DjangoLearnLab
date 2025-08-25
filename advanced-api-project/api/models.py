from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.utils import timezone

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: CharField to store the author's full name (max 100 characters)
    
    Relationships:
    - One-to-many relationship with Book model (an author can have multiple books)
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: CharField for the book's title (max 200 characters)
    - publication_year: IntegerField for the year the book was published
    - author: ForeignKey linking to the Author model (many-to-one relationship)
    
    Validation:
    - Custom validation ensures publication_year is not in the future
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # Delete books when author is deleted
        related_name='books'  # Allows accessing books via author.books
    )
    
    def clean(self):
        """Validate that publication_year is not in the future"""
        current_year = timezone.now().year
        if self.publication_year > current_year:
            raise ValidationError({
                'publication_year': f'Publication year cannot be in the future. Current year is {current_year}.'
            })
    
    def save(self, *args, **kwargs):
        """Override save to run full validation"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        # Ensure unique constraint for book titles by same author
        unique_together = ['title', 'author']