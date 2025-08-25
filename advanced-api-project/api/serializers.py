from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer serializes all fields of the Book model.
    
    Includes custom validation to ensure publication_year is not in the future.
    
    Fields:
    - id: Primary key (auto-generated)
    - title: Book title
    - publication_year: Year of publication
    - author: Foreign key reference to Author
    
    Validation:
    - Custom validate_publication_year method checks for future years
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields from the Book model
    
    def validate_publication_year(self, value):
        """
        Custom validation method to ensure publication_year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer serializes Author model with nested BookSerializer.
    
    Fields:
    - id: Primary key (auto-generated)
    - name: Author's name
    - books: Nested serialization of related Book objects using BookSerializer
    
    The relationship between Author and Book is handled through:
    1. The ForeignKey relationship defined in the Book model
    2. The 'related_name="books"' attribute allows accessing books via author.books
    3. Nested serialization includes all book details within the author serialization
    """
    
    # Nested serializer for related books - read_only allows creation through BookSerializer
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include id, name, and nested books