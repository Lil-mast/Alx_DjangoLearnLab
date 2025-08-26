# Testing Documentation

## Overview

This document describes the testing strategy and how to run tests for the Advanced API Project.

## Test Structure

The test suite is organized into multiple test files:

- `test_models.py`: Tests for database models and validation
- `test_serializers.py`: Tests for serializers and data validation
- `test_views.py`: Tests for API endpoints and CRUD operations
- `test_permissions.py`: Tests for authentication and permissions
- `utils.py`: Test utilities and setup mixin

## Running Tests

### Run All Tests
```bash
python manage.py test api

## Login-Based Authentication Testing

The test suite now includes comprehensive login-based authentication tests:

### Session Authentication Tests
- `test_book_create_with_login`: Tests book creation using `client.login()`
- `test_book_update_with_login`: Tests book updates with session login
- `test_book_delete_with_login`: Tests book deletion with session login
- `test_book_create_with_wrong_password`: Tests authentication failure
- `test_session_persistence_across_requests`: Tests session persistence

### Login/Logout State Tests
- `test_user_state_after_logout`: Verifies proper session cleanup
- `test_book_operations_after_logout`: Tests operations fail after logout
- `test_read_operations_dont_require_login`: Tests public access to read endpoints

### Mixed Authentication Tests
- `test_mixed_authentication_methods`: Compares session auth vs force_authenticate
- `test_multiple_operations_with_same_session`: Tests multiple operations in one session

### Running Login Tests
```bash
# Run specific login tests
python manage.py test api.tests.BookAPITestCase.test_book_create_with_login
python manage.py test api.tests.BookAPITestCase.test_session_persistence_across_requests

# Run all login-related tests
python manage.py test api.tests -k "login"