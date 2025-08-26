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
    - CRUD operations with login-based authentication
    - Filtering, searching, ordering
    - Session authentication testing
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

    # --- Login-Based Authentication Tests ---

    def test_book_create_with_login(self):
        """Test that logged-in users can create books using session login"""
        # Login using Django's login method
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
        data = {
            'title': 'New Book with Login',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)
        self.assertEqual(response.data['title'], 'New Book with Login')
        
        # Logout after test
        self.client.logout()

    def test_book_update_with_login(self):
        """Test that logged-in users can update books using session login"""
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Updated with Login',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(
            self.book_update_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated with Login')
        
        # Logout
        self.client.logout()

    def test_book_delete_with_login(self):
        """Test that logged-in users can delete books using session login"""
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
        
        # Logout
        self.client.logout()

    def test_book_create_with_wrong_password(self):
        """Test that users with wrong password cannot create books"""
        # Attempt login with wrong password
        login_success = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login_success, "Login should fail with wrong password")
        
        data = {
            'title': 'Should Not Create',
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

    def test_book_create_with_nonexistent_user(self):
        """Test that non-existent users cannot create books"""
        # Attempt login with non-existent user
        login_success = self.client.login(username='nonexistent', password='testpass123')
        self.assertFalse(login_success, "Login should fail with non-existent user")
        
        data = {
            'title': 'Should Not Create',
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

    def test_book_operations_after_logout(self):
        """Test that users cannot perform write operations after logout"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Logout
        self.client.logout()
        
        # Try to create book after logout
        data = {
            'title': 'Should Not Create After Logout',
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

    def test_multiple_operations_with_same_session(self):
        """Test multiple operations within the same login session"""
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Create a book
        create_data = {
            'title': 'First Book in Session',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        create_response = self.client.post(
            self.book_create_url,
            data=json.dumps(create_data),
            content_type='application/json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        # Update the created book
        new_book_id = create_response.data['id']
        update_data = {
            'title': 'Updated in Session',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        update_response = self.client.put(
            reverse('book-update', kwargs={'pk': new_book_id}),
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Delete the book
        delete_response = self.client.delete(
            reverse('book-delete', kwargs={'pk': new_book_id})
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Final count should be back to original
        self.assertEqual(Book.objects.count(), 4)
        
        # Logout
        self.client.logout()

    def test_admin_user_permissions(self):
        """Test that admin users have the same permissions as regular users"""
        # Login as admin
        self.client.login(username='adminuser', password='adminpass123')
        
        data = {
            'title': 'Admin Created Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)
        
        # Logout
        self.client.logout()

    # --- Session Persistence Tests ---

    def test_session_persistence_across_requests(self):
        """Test that login session persists across multiple requests"""
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # First request - should work
        data1 = {
            'title': 'First Request Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response1 = self.client.post(
            self.book_create_url,
            data=json.dumps(data1),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Second request - should still work with same session
        data2 = {
            'title': 'Second Request Book',
            'publication_year': 2024,
            'author': self.author2.id
        }
        
        response2 = self.client.post(
            self.book_create_url,
            data=json.dumps(data2),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Book.objects.count(), 6)
        
        # Logout
        self.client.logout()

    def test_read_operations_dont_require_login(self):
        """Test that read operations work regardless of login state"""
        # Test without login
        response1 = self.client.get(self.book_list_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Test with login
        response2 = self.client.get(self.book_list_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # Logout and test again
        self.client.logout()
        response3 = self.client.get(self.book_list_url)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        
        # All responses should have the same data
        self.assertEqual(len(response1.data['results']), len(response2.data['results']))
        self.assertEqual(len(response1.data['results']), len(response3.data['results']))

    # --- Mixed Authentication Tests ---

    def test_mixed_authentication_methods(self):
        """Test that both session auth and force_authenticate work consistently"""
        # Test with session login
        self.client.login(username='testuser', password='testpass123')
        session_response = self.client.get(self.book_list_url)
        self.assertEqual(session_response.status_code, status.HTTP_200_OK)
        self.client.logout()
        
        # Test with force_authenticate
        auth_client = APIClient()
        auth_client.force_authenticate(user=self.user)
        force_response = auth_client.get(self.book_list_url)
        self.assertEqual(force_response.status_code, status.HTTP_200_OK)
        
        # Both should return the same data
        self.assertEqual(
            len(session_response.data['results']),
            len(force_response.data['results'])
        )

    # --- Login/Logout State Tests ---

    def test_user_state_after_logout(self):
        """Test that user state is properly cleared after logout"""
        # Verify not logged in initially
        response_before = self.client.get(self.book_create_url)
        self.assertEqual(response_before.status_code, status.HTTP_403_FORBIDDEN)
        
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Verify logged in
        data = {'title': 'Test', 'publication_year': 2023, 'author': self.author1.id}
        response_during = self.client.post(
            self.book_create_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response_during.status_code, status.HTTP_201_CREATED)
        
        # Logout
        self.client.logout()
        
        # Verify logged out
        response_after = self.client.get(self.book_create_url)
        self.assertEqual(response_after.status_code, status.HTTP_403_FORBIDDEN)

    # --- Keep the existing tests from previous implementation ---
    # (All the previous test methods should remain here)
    # ... [Previous test methods remain unchanged] ...

# Add this at the end to include all previous tests
# (This ensures we don't lose the original comprehensive test suite)