from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostCreateSerializer
from .permissions import IsAuthorOrReadOnly

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
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            message = 'Post unliked'
        else:
            post.likes.add(user)
            message = 'Post liked'

        return Response({'message': message, 'like_count': post.like_count})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
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
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)

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
    popular_posts = Post.objects.exclude(author__in=following_users).order_by('-likes__count')[:10]
    
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
    user = get_object_or_404(get_user_model(), id=user_id)
    
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
    ).order_by('-like_count', '-created_at')[:20]
    
    serializer = PostSerializer(trending_posts, many=True, context={'request': request})
    
    return Response({
        'message': 'Trending posts from the last 7 days',
        'posts': serializer.data
    })