# Like and Notification System Documentation

## Like Endpoints

### Like/Unlike a Post
**POST** `/api/posts/<post_id>/like/`
- Toggles like status
- Returns: `{message, liked, like_count}`

### Get Post Likes
**GET** `/api/posts/<post_id>/likes/`
- Returns all likes for a post

### Get User's Liked Posts
**GET** `/api/user/likes/`
- Returns all posts liked by current user

## Notification Endpoints

### List Notifications
**GET** `/api/notifications/`
- Returns all notifications for current user

### List Unread Notifications
**GET** `/api/notifications/unread/`
- Returns only unread notifications

### Mark Notification as Read
**POST** `/api/notifications/<notification_id>/read/`

### Mark All Notifications as Read
**POST** `/api/notifications/read-all/`

### Notification Statistics
**GET** `/api/notifications/stats/`
- Returns: `{total_notifications, unread_notifications, read_notifications}`

## Notification Types
- `follow`: User started following you
- `like`: User liked your post
- `comment`: User commented on your post
- `mention`: User mentioned you
- `share`: User shared your post