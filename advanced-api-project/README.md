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