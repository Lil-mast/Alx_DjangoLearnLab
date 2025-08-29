# Posts API Documentation

## Endpoints

### Posts

- **GET /api/posts/** - List all posts (supports pagination, search, filtering)
- **POST /api/posts/** - Create a new post
- **GET /api/posts/{id}/** - Get specific post
- **PUT /api/posts/{id}/** - Update post
- **DELETE /api/posts/{id}/** - Delete post
- **POST /api/posts/{id}/like/** - Like/unlike post

### Comments

- **GET /api/posts/{post_id}/comments/** - List comments for a post
- **POST /api/posts/{post_id}/comments/** - Create comment on a post
- **GET /api/posts/{post_id}/comments/{id}/** - Get specific comment
- **PUT /api/posts/{post_id}/comments/{id}/** - Update comment
- **DELETE /api/posts/{post_id}/comments/{id}/** - Delete comment

## Query Parameters

- `search`: Search in title and content
- `author`: Filter by author ID
- `ordering`: Order by fields (created_at, updated_at, like_count)
- `page`: Page number for pagination

## Example Requests

### Create Post
```json
POST /api/posts/
{
  "title": "My Post",
  "content": "Post content here"
}

# Social Media API Documentation

## Follow Management Endpoints

### Follow a User
**POST** `/api/auth/follow/<user_id>/`

**Response:**
```json
{
    "message": "Successfully followed username",
    "following": true,
    "followers_count": 5,
    "following_count": 10
}