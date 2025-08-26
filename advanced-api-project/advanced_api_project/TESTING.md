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