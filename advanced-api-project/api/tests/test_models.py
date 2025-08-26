from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import Author, Book

class ModelTestCase(TestCase):
    """Test cases for Author and Book models"""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
    
    def test_author_creation(self):
        """Test that Author model can be created successfully"""
        self.assertEqual(self.author.name, 'Test Author')
        self.assertEqual(str(self.author), 'Test Author')
    
    def test_book_creation(self):
        """Test that Book model can be created successfully"""
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publication_year, 2020)
        self.assertEqual(book.author, self.author)
        self.assertEqual(str(book), 'Test Book (2020)')
    
    def test_book_future_publication_year_validation(self):
        """Test that book with future publication year raises validation error"""
        future_year = timezone.now().year + 1
        
        book = Book(
            title='Future Book',
            publication_year=future_year,
            author=self.author
        )
        
        with self.assertRaises(ValidationError):
            book.full_clean()
    
    def test_book_author_relationship(self):
        """Test the one-to-many relationship between Author and Book"""
        book1 = Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=self.author
        )
        
        book2 = Book.objects.create(
            title='Book 2',
            publication_year=2021,
            author=self.author
        )
        
        # Test reverse relationship
        self.assertEqual(self.author.books.count(), 2)
        self.assertIn(book1, self.author.books.all())
        self.assertIn(book2, self.author.books.all())