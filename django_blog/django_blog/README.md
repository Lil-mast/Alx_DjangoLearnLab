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