from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from django.utils import timezone
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for Book API endpoints including:
    - CRUD operations
    - Filtering, searching, ordering
    - Authentication and permissions
    - Validation
    """
    
    def setUp(self):
        """Set up test data that will be used across all test cases"""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        self.author3 = Author.objects.create(name='Stephen King')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        self.book4 = Book.objects.create(
            title='The Shining',
            publication_year=1977,
            author=self.author3
        )
        
        # API client instances
        self.client = APIClient()  # Unauthenticated client
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)  # Authenticated client
        
        # URL patterns
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        
        self.author_list_url = reverse('author-list')
        self.author_detail_url = reverse('author-detail', kwargs={'pk': self.author1.pk})

    def tearDown(self):
        """Clean up after tests"""
        User.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()

    # --- CRUD Operation Tests ---

    def test_book_list_unauthenticated(self):
        """Test that unauthenticated users can access book list"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

    def test_book_detail_unauthenticated(self):
        """Test that unauthenticated users can access book detail"""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], 1997)
        self.assertEqual(response.data['author'], self.author1.id)

    def test_book_create_authenticated(self):
        """Test that authenticated users can create books"""
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.auth_client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(response.data['author'], self.author1.id)

    def test_book_create_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4)

    def test_book_update_authenticated(self):
        """Test that authenticated users can update books"""
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.auth_client.put(
            self.book_update_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_book_update_unauthenticated(self):
        """Test that unauthenticated users cannot update books"""
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(
            self.book_update_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Unauthorized Update')

    def test_book_delete_authenticated(self):
        """Test that authenticated users can delete books"""
        response = self.auth_client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_book_delete_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())

    # --- Filtering Tests ---

    def test_filter_by_author(self):
        """Test filtering books by author ID"""
        response = self.client.get(f"{self.book_list_url}?author={self.author1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.id)

    def test_filter_by_publication_year(self):
        """Test filtering books by publication year"""
        response = self.client.get(f"{self.book_list_url}?publication_year=1997")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)

    def test_filter_by_publication_year_range(self):
        """Test filtering books by publication year range"""
        response = self.client.get(f"{self.book_list_url}?publication_year__gte=1990&publication_year__lte=2000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 1997, 1998, 1996

    def test_filter_by_author_name(self):
        """Test filtering books by author name (contains)"""
        response = self.client.get(f"{self.book_list_url}?author_name=rowling")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_title(self):
        """Test filtering books by title (contains)"""
        response = self.client.get(f"{self.book_list_url}?title=harry")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    # --- Search Tests ---

    def test_search_by_title(self):
        """Test searching books by title"""
        response = self.client.get(f"{self.book_list_url}?search=harry")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_by_author_name(self):
        """Test searching books by author name"""
        response = self.client.get(f"{self.book_list_url}?search=king")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Shining')

    # --- Ordering Tests ---

    def test_ordering_by_title_ascending(self):
        """Test ordering books by title (ascending)"""
        response = self.client.get(f"{self.book_list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_title_descending(self):
        """Test ordering books by title (descending)"""
        response = self.client.get(f"{self.book_list_url}?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_ordering_by_publication_year_ascending(self):
        """Test ordering books by publication year (ascending)"""
        response = self.client.get(f"{self.book_list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))

    def test_ordering_by_publication_year_descending(self):
        """Test ordering books by publication year (descending)"""
        response = self.client.get(f"{self.book_list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_ordering_by_multiple_fields(self):
        """Test ordering books by multiple fields"""
        response = self.client.get(f"{self.book_list_url}?ordering=author__name,title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by author name first, then title

    # --- Validation Tests ---

    def test_book_create_with_future_publication_year(self):
        """Test that books with future publication years are rejected"""
        future_year = timezone.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        
        response = self.auth_client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertEqual(Book.objects.count(), 4)

    def test_book_create_with_invalid_author(self):
        """Test that books with invalid author IDs are rejected"""
        data = {
            'title': 'Invalid Author Book',
            'publication_year': 2023,
            'author': 9999  # Non-existent author ID
        }
        
        response = self.auth_client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('author', response.data)
        self.assertEqual(Book.objects.count(), 4)

    def test_book_create_with_missing_required_fields(self):
        """Test that books with missing required fields are rejected"""
        data = {
            'title': 'Missing Fields Book',
            # Missing publication_year and author
        }
        
        response = self.auth_client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('author', response.data)
        self.assertEqual(Book.objects.count(), 4)

    # --- Author Endpoint Tests ---

    def test_author_list_unauthenticated(self):
        """Test that unauthenticated users can access author list"""
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_author_detail_unauthenticated(self):
        """Test that unauthenticated users can access author detail"""
        response = self.client.get(self.author_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 2)
        self.assertEqual(response.data['books'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')

    def test_author_filtering(self):
        """Test filtering authors by name"""
        response = self.client.get(f"{self.author_list_url}?name=King")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Stephen King')

    def test_author_search(self):
        """Test searching authors by name"""
        response = self.client.get(f"{self.author_list_url}?search=rowling")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'J.K. Rowling')

    def test_author_ordering(self):
        """Test ordering authors by name"""
        response = self.client.get(f"{self.author_list_url}?ordering=name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [author['name'] for author in response.data['results']]
        self.assertEqual(names, sorted(names))

    # --- Edge Case Tests ---

    def test_nonexistent_book_detail(self):
        """Test accessing detail of non-existent book"""
        response = self.client.get(reverse('book-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_book_update(self):
        """Test updating non-existent book"""
        data = {
            'title': 'Nonexistent Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.auth_client.put(
            reverse('book-update', kwargs={'pk': 9999}),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_book_delete(self):
        """Test deleting non-existent book"""
        response = self.auth_client.delete(reverse('book-delete', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_search_results(self):
        """Test search that returns no results"""
        response = self.client.get(f"{self.book_list_url}?search=nonexistentterm")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_empty_filter_results(self):
        """Test filter that returns no results"""
        response = self.client.get(f"{self.book_list_url}?publication_year=1900")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)