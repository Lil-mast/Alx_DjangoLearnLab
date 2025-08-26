from doctest import DocTestCase
import json
from django.urls import reverse
from rest_framework import status
from .utils import TestSetupMixin
from ..models import Book

class BookViewTestCase(TestSetupMixin, DocTestCase):
    """Test cases for Book API views"""
    
    def test_book_list_unauthenticated(self):
        """Test that unauthenticated users can access book list"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_book_list_filtering(self):
        """Test filtering functionality"""
        # Filter by author
        response = self.client.get(f"{self.book_list_url}?author={self.author1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Filter by publication year
        response = self.client.get(f"{self.book_list_url}?publication_year=1997")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_book_list_search(self):
        """Test search functionality"""
        response = self.client.get(f"{self.book_list_url}?search=Harry")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_book_list_ordering(self):
        """Test ordering functionality"""
        # Order by title ascending
        response = self.client.get(f"{self.book_list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
        
        # Order by publication year descending
        response = self.client.get(f"{self.book_list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_book_detail_unauthenticated(self):
        """Test that unauthenticated users can access book detail"""
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_book_create_authenticated(self):
        """Test that authenticated users can create books"""
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.authenticated_client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Test Book')
    
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
        self.assertEqual(Book.objects.count(), 3)
    
    def test_book_update_authenticated(self):
        """Test that authenticated users can update books"""
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.authenticated_client.put(
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
        response = self.authenticated_client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_book_delete_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_book_create_with_future_year(self):
        """Test that books with future publication years are rejected"""
        future_year = 2030
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        
        response = self.authenticated_client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

class AuthorViewTestCase(TestSetupMixin, DocTestCase):
    """Test cases for Author API views"""
    
    def test_author_list_unauthenticated(self):
        """Test that unauthenticated users can access author list"""
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_author_detail_unauthenticated(self):
        """Test that unauthenticated users can access author detail"""
        response = self.client.get(self.author_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 2)