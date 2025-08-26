from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from ..models import Author, Book
from ..serializers import BookSerializer, AuthorSerializer

class SerializerTestCase(TestCase):
    """Test cases for serializers"""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
    
    def test_book_serializer_valid_data(self):
        """Test BookSerializer with valid data"""
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_book_serializer_future_year_validation(self):
        """Test BookSerializer validation for future publication year"""
        future_year = timezone.now().year + 1
        
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }
        
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
    
    def test_author_serializer_with_books(self):
        """Test AuthorSerializer includes nested books"""
        Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=self.author
        )
        
        Book.objects.create(
            title='Book 2',
            publication_year=2021,
            author=self.author
        )
        
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Author')
        self.assertEqual(len(data['books']), 2)
        self.assertEqual(data['books'][0]['title'], 'Book 1')