# Advanced API Project

## API Endpoints

### Books

- `GET /api/books/` - List all books (public access)
- `GET /api/books/<id>/` - Get specific book details (public access)
- `POST /api/books/create/` - Create new book (authenticated users only)
- `PUT /api/books/<id>/update/` - Update existing book (authenticated users only)
- `DELETE /api/books/<id>/delete/` - Delete book (authenticated users only)

### Authors

- `GET /api/authors/` - List all authors (public access)
- `GET /api/authors/<id>/` - Get specific author details (public access)

## Features

- **CRUD Operations**: Full Create, Read, Update, Delete functionality for Books
- **Permissions**: Read-only for public, full access for authenticated users
- **Filtering**: Filter by publication_year and author__name
- **Searching**: Search by title and author name
- **Ordering**: Order by title, publication_year, or author name

## Authentication

Use Basic Authentication or Session Authentication for protected endpoints:

```bash
curl -u username:password http://localhost:8000/api/books/create/

# Advanced API Project - Filtering, Searching & Ordering

## Enhanced Book API Endpoints

### Filtering Capabilities

The Book list endpoint supports advanced filtering:

#### Basic Filtering:
- `?publication_year=1997` - Exact year match
- `?author=1` - Books by specific author ID
- `?author_name=rowling` - Books by author name (case-insensitive contains)

#### Range Filtering:
- `?publication_year__gt=2000` - Years greater than 2000
- `?publication_year__lt=2020` - Years less than 2020
- `?publication_year__gte=1990&publication_year__lte=2000` - Years between 1990-2000

#### Title Filtering:
- `?title=potter` - Books with "potter" in title (case-insensitive)

### Search Functionality

Full-text search across multiple fields:
- `?search=harry` - Search in title and author name fields
- Supports: exact match, starts-with, and case-sensitive variants

### Ordering Options

Sort results by various fields:
- `?ordering=title` - Ascending by title
- `?ordering=-publication_year` - Descending by publication year
- `?ordering=author__name,title` - Multiple field ordering

### Combined Parameters

All parameters can be combined: