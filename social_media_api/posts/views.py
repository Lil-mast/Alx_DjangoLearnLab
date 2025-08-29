from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, PostCreateSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'like_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Using generics.get_object_or_404(Post, pk=pk) as requested
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user

        # Using Like.objects.get_or_create as requested
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            # Using Notification.objects.create as requested
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb=Notification.LIKE,
                    target=post,
                    timestamp=timezone.now()
                )
            message = 'Post liked'
            liked = True
        else:
            like.delete()
            message = 'Post unliked'
            liked = False

        return Response({
            'message': message,
            'liked': liked,
            'like_count': post.likes_received.count()
        })

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Get all likes for a post"""
        # Using generics.get_object_or_404 as requested
        post = generics.get_object_or_404(Post, pk=pk)
        likes = post.likes_received.all()
        serializer = LikeSerializer(likes, many=True)
        return Response({
            'post_id': post.id,
            'like_count': likes.count(),
            'likes': serializer.data
        })

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        # Using generics.get_object_or_404 as requested
        post = generics.get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        # Using generics.get_object_or_404 as requested
        post = generics.get_object_or_404(Post, pk=self.kwargs['post_pk'])
        comment = serializer.save(author=self.request.user, post=post)
        
        # Using Notification.objects.create as requested
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb=Notification.COMMENT,
                target=post,
                timestamp=timezone.now()
            )

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        # Using generics.get_object_or_404 as requested
        post = generics.get_object_or_404(Post, id=post_id)
        
        # Using Like.objects.get_or_create as requested
        like, created = Like.objects.get_or_create(
            user=self.request.user, 
            post=post
        )
        
        if created:
            # Using Notification.objects.create as requested
            if post.author != self.request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=self.request.user,
                    verb=Notification.LIKE,
                    target=post,
                    timestamp=timezone.now()
                )
            serializer.instance = like
        else:
            return Response(
                {'error': 'You have already liked this post'},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_likes(request):
    """Get all posts liked by the current user"""
    likes = Like.objects.filter(user=request.user).select_related('post')
    posts = [like.post for like in likes]
    
    serializer = PostSerializer(
        posts, 
        many=True, 
        context={'request': request}
    )
    
    return Response({
        'total_likes': likes.count(),
        'liked_posts': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """
    Get feed of posts from users that the current user follows
    """
    # Get users that the current user follows using following.all()
    following_users = request.user.following.all()
    
    # Use Post.objects.filter(author__in=following_users).order_by as requested
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Apply pagination
    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 10)
    
    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        page = 1
        page_size = 10
    
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    paginated_posts = posts[start_index:end_index]
    
    serializer = PostSerializer(
        paginated_posts, 
        many=True, 
        context={'request': request}
    )
    
    return Response({
        'page': page,
        'page_size': page_size,
        'total_posts': posts.count(),
        'has_next': end_index < posts.count(),
        'has_previous': page > 1,
        'following_count': following_users.count(),
        'posts': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def explore_feed(request):
    """
    Get explore feed with posts from users not followed by current user
    """
    # Get users that the current user doesn't follow using following.all()
    following_users = request.user.following.all()
    
    # Use Post.objects.filter with exclusion and order_by
    posts = Post.objects.exclude(
        Q(author=request.user) | Q(author__in=following_users)
    ).order_by('-created_at')[:20]
    
    serializer = PostSerializer(posts, many=True, context={'request': request})
    
    return Response({
        'message': 'Explore feed - posts from users you don\'t follow',
        'posts': serializer.data,
        'following_count': following_users.count()
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def personalized_feed(request):
    """
    Personalized feed with posts from followed users and popular posts
    """
    # Using following.all() as requested
    following_users = request.user.following.all()
    
    # Using Post.objects.filter(author__in=following_users).order_by as requested
    followed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Get popular posts (posts with most likes)
    popular_posts = Post.objects.exclude(author__in=following_users).order_by('-likes_received__count')[:10]
    
    # Combine and order the posts
    all_posts = list(followed_posts) + list(popular_posts)
    all_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    # Apply pagination
    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 15)
    
    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        page = 1
        page_size = 15
    
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    paginated_posts = all_posts[start_index:end_index]
    
    serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
    
    return Response({
        'page': page,
        'page_size': page_size,
        'total_posts': len(all_posts),
        'followed_posts_count': followed_posts.count(),
        'popular_posts_count': popular_posts.count(),
        'following_count': following_users.count(),
        'posts': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_posts_feed(request, user_id):
    """
    Get feed of posts from a specific user
    """
    # Using generics.get_object_or_404 as requested
    user = generics.get_object_or_404(get_user_model(), id=user_id)
    
    # Check if current user follows this user using following.all()
    is_following = request.user.following.all().filter(id=user_id).exists()
    
    # Using Post.objects.filter with order_by
    posts = Post.objects.filter(author=user).order_by('-created_at')
    
    serializer = PostSerializer(posts, many=True, context={'request': request})
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'is_following': is_following
        },
        'posts_count': posts.count(),
        'posts': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def trending_posts(request):
    """
    Get trending posts (most liked posts in recent time)
    """
    # Using Post.objects.filter with order_by for trending
    trending_posts = Post.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).order_by('-likes_received__count', '-created_at')[:20]
    
    serializer = PostSerializer(trending_posts, many=True, context={'request': request})
    
    return Response({
        'message': 'Trending posts from the last 7 days',
        'posts': serializer.data
    })