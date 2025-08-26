from doctest import DocTestCase
from django.urls import reverse
from rest_framework import status
from .utils import TestSetupMixin

class PermissionTestCase(TestSetupMixin, DocTestCase):
    """Test cases for API permissions"""
    
    def test_read_endpoints_public_access(self):
        """Test that read endpoints are accessible without authentication"""
        endpoints = [
            reverse('book-list'),
            reverse('book-detail', kwargs={'pk': self.book1.pk}),
            reverse('author-list'),
            reverse('author-detail', kwargs={'pk': self.author1.pk}),
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code, 
                status.HTTP_200_OK,
                f"Failed for endpoint: {endpoint}"
            )
    
    def test_write_endpoints_require_authentication(self):
        """Test that write endpoints require authentication"""
        write_endpoints = [
            (reverse('book-create'), 'post'),
            (reverse('book-update', kwargs={'pk': self.book1.pk}), 'put'),
            (reverse('book-delete', kwargs={'pk': self.book1.pk}), 'delete'),
        ]
        
        for endpoint, method in write_endpoints:
            if method == 'post':
                response = self.client.post(endpoint, {})
            elif method == 'put':
                response = self.client.put(endpoint, {})
            elif method == 'delete':
                response = self.client.delete(endpoint)
            
            self.assertEqual(
                response.status_code, 
                status.HTTP_403_FORBIDDEN,
                f"Failed for endpoint: {endpoint} with method: {method}"
            )
    
    def test_authenticated_users_can_access_write_endpoints(self):
        """Test that authenticated users can access write endpoints"""
        data = {
            'title': 'Auth Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        # Test create
        response = self.authenticated_client.post(
            reverse('book-create'),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test update
        response = self.authenticated_client.put(
            reverse('book-update', kwargs={'pk': self.book1.pk}),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test delete
        response = self.authenticated_client.delete(
            reverse('book-delete', kwargs={'pk': self.book2.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)