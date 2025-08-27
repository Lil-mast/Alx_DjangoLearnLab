# Django Blog Authentication System

## Overview

This Django blog application features a complete user authentication system with registration, login, logout, and profile management functionality. The system extends Django's built-in authentication with custom forms and additional user profile fields.

## Features

- **User Registration**: Custom registration form with email validation
- **User Login/Logout**: Secure session-based authentication
- **Profile Management**: Extended user profiles with bio and profile picture
- **CSRF Protection**: All forms include CSRF token protection
- **Password Security**: Uses Django's built-in PBKDF2 hashing algorithm
- **Responsive Design**: Styled templates with CSS
- **Flash Messages**: User feedback for successful operations and errors

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default), PostgreSQL/MySQL ready
- **Templates**: Django Template Language (DTL)
- **Static Files**: CSS, JavaScript
- **Authentication**: Django built-in auth with custom extensions

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtualenv (recommended)

### Installation Steps

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd django_blog

## Blog Post CRUD Operations

### Features
- **Create**: Authenticated users can create new blog posts
- **Read**: All users can view blog posts (list and detail views)
- **Update**: Post authors can edit their own posts
- **Delete**: Post authors can delete their own posts

### Permissions
- **Public Access**: Anyone can view posts (list and detail)
- **Authenticated Users**: Can create new posts
- **Post Authors**: Can edit and delete their own posts

### URL Endpoints

| Endpoint | Method | Description | Access |
|----------|--------|-------------|---------|
| `/posts/` | GET | List all blog posts | Public |
| `/posts/new/` | GET/POST | Create new post | Authenticated only |
| `/posts/<int:pk>/` | GET | View specific post | Public |
| `/posts/<int:pk>/edit/` | GET/POST | Edit post | Author only |
| `/posts/<int:pk>/delete/` | GET/POST | Delete post | Author only |

### Testing CRUD Operations

#### 1. Create Post Test
1. Log in with valid credentials
2. Navigate to `/posts/new/`
3. Fill in title and content
4. Submit form
5. Verify post appears in list

#### 2. Read Post Test
1. Navigate to `/posts/` (verify post list)
2. Click on any post title (verify detail view)
3. Verify all post information displays correctly

#### 3. Update Post Test
1. Log in as post author
2. Navigate to post detail page
3. Click "Edit Post"
4. Modify title/content and submit
5. Verify changes persist

#### 4. Delete Post Test
1. Log in as post author
2. Navigate to post detail page
3. Click "Delete Post"
4. Confirm deletion
5. Verify post removed from list

#### 5. Permission Tests
- Try editing another user's post (should fail)
- Try deleting another user's post (should fail)
- Try creating post without logging in (should redirect to login)

## Comment System

### Features
- **Add Comments**: Authenticated users can comment on blog posts
- **Edit Comments**: Comment authors can edit their own comments
- **Delete Comments**: Comment authors can delete their own comments (soft delete)
- **Like Comments**: Users can like/unlike comments
- **Real-time Updates**: AJAX-based like functionality

### Permissions
- **Public Access**: Anyone can view comments
- **Authenticated Users**: Can add comments and like/unlike comments
- **Comment Authors**: Can edit and delete their own comments

### URL Endpoints

| Endpoint | Method | Description | Access |
|----------|--------|-------------|---------|
| `/posts/<int:pk>/comment/` | POST | Add comment to post | Authenticated |
| `/comments/<int:pk>/edit/` | GET/POST | Edit comment | Author only |
| `/comments/<int:pk>/delete/` | GET/POST | Delete comment | Author only |
| `/comments/<int:pk>/like/` | POST | Like/unlike comment | Authenticated |

### Testing Comment Functionality

#### 1. Add Comment Test
1. Log in with valid credentials
2. Navigate to any post detail page
3. Fill in comment form and submit
4. Verify comment appears in comments section

#### 2. Edit Comment Test
1. Log in as comment author
2. Navigate to post with your comment
3. Click "Edit" on your comment
4. Modify content and submit
5. Verify changes persist

#### 3. Delete Comment Test
1. Log in as comment author
2. Navigate to post with your comment
3. Click "Delete" on your comment
4. Confirm deletion
5. Verify comment is removed

#### 4. Like Comment Test
1. Log in with valid credentials
2. Navigate to any post with comments
3. Click like button on a comment
4. Verify like count updates
5. Click again to unlike

#### 5. Permission Tests
- Try editing another user's comment (should fail)
- Try deleting another user's comment (should fail)
- Try commenting without logging in (should see login prompt)

## Tagging and Search Features

### Tagging System

#### Features
- **Tag Management**: Create, edit, and delete tags
- **Tag Association**: Multiple tags per post, multiple posts per tag
- **Tag Navigation**: Click tags to view all posts with that tag
- **Tag Cloud**: Visual display of all available tags

#### How to Use Tags
1. **Adding Tags**: When creating/editing a post, enter tags separated by commas
2. **Viewing Tags**: Tags appear below post titles and can be clicked to filter posts
3. **Managing Tags**: Tags are automatically created when used and managed through the admin interface

#### URL Endpoints
- `/tags/<slug:slug>/` - View all posts with a specific tag

### Search Functionality

#### Features
- **Full-text Search**: Search across post titles, content, and tags
- **Instant Results**: Real-time search results
- **Advanced Filtering**: Complex query lookups using Django's Q objects

#### How to Use Search
1. **Search Bar**: Use the search bar in the navigation menu
2. **Search Terms**: Enter keywords, phrases, or tag names
3. **Results**: View filtered posts matching your search criteria

#### URL Endpoints
- `/search/?q=query` - Search for posts containing the query

### Testing Guidelines

#### Tagging Tests
1. **Create Post with Tags**: Verify tags are saved and displayed correctly
2. **Edit Post Tags**: Verify tag updates persist
3. **Tag Navigation**: Click tags to verify filtering works
4. **Duplicate Tags**: Test handling of duplicate tag names

#### Search Tests
1. **Basic Search**: Test searching by title keywords
2. **Content Search**: Test searching by content phrases
3. **Tag Search**: Test searching by tag names
4. **Empty Results**: Test search with no matches
5. **Special Characters**: Test search with special characters

### Database Schema
The tagging system uses a many-to-many relationship:
- `Tag` model with name and slug fields
- `Post.tags` field linking to Tag model
- Automatic slug generation for SEO-friendly URLs

### Performance Considerations
- Indexes on frequently searched fields
- Distinct results to avoid duplicates
- Pagination for large result sets