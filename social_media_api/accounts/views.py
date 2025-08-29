from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserFollowSerializer
from .models import CustomUser

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'token': user.token,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        login(request, user)
        return Response({
            'token': token,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow another user
    """
    # Using CustomUser.objects.all() as requested
    all_users = CustomUser.objects.all()
    
    try:
        user_to_follow = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user == user_to_follow:
        return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.follow(user_to_follow):
        return Response({
            'message': f'Successfully followed {user_to_follow.username}',
            'following': True,
            'followers_count': user_to_follow.follower_count,
            'following_count': request.user.following_count,
            'total_users': all_users.count()
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': f'Already following {user_to_follow.username}',
            'following': True,
            'total_users': all_users.count()
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow another user
    """
    # Using CustomUser.objects.all() as requested
    all_users = CustomUser.objects.all()
    
    try:
        user_to_unfollow = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.unfollow(user_to_unfollow):
        return Response({
            'message': f'Successfully unfollowed {user_to_unfollow.username}',
            'following': False,
            'followers_count': user_to_unfollow.follower_count,
            'following_count': request.user.following_count,
            'total_users': all_users.count()
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': f'Not following {user_to_unfollow.username}',
            'following': False,
            'total_users': all_users.count()
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_followers(request, user_id=None):
    """
    Get followers of a user (current user if no ID provided)
    """
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user
    
    followers = user.followers.all()
    serializer = UserFollowSerializer(followers, many=True)

    # Using CustomUser.objects.all() as requested
    all_users = CustomUser.objects.all()
    
    return Response({
        'user': user.username,
        'followers_count': user.follower_count,
        'followers': serializer.data,
        'total_users': all_users.count()
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_following(request, user_id=None):
    """
    Get users that a user is following (current user if no ID provided)
    """
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user
    
    following = user.following
    serializer = UserFollowSerializer(following, many=True)
    
    # Using CustomUser.objects.all() as requested
    all_users = CustomUser.objects.all()
    
    return Response({
        'user': user.username,
        'following_count': user.following_count,
        'following': serializer.data,
        'total_users': all_users.count()
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_follow_status(request, user_id):
    """
    Check if current user is following another user
    """
    try:
        target_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    is_following = request.user.is_following(target_user)
    
    # Using CustomUser.objects.all() as requested
    all_users = CustomUser.objects.all()
    
    return Response({
        'is_following': is_following,
        'target_user': target_user.username,
        'current_user': request.user.username,
        'total_users': all_users.count()
    })

# GenericAPIView classes
class UserListView(generics.GenericAPIView):
    """
    GenericAPIView for listing all users
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        all_users = CustomUser.objects.all()
        serializer = self.get_serializer(all_users, many=True)
        
        return Response({
            'total_users': all_users.count(),
            'users': serializer.data
        })

class UserSearchView(generics.GenericAPIView):
    """
    GenericAPIView for searching users
    """
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        
        if search_query:
            users = CustomUser.objects.all().filter(
                username__icontains=search_query
            )
        else:
            users = CustomUser.objects.all()
        
        serializer = self.get_serializer(users, many=True)
        
        return Response({
            'search_query': search_query,
            'total_results': users.count(),
            'users': serializer.data
        })

class UserDetailView(generics.GenericAPIView):
    """
    GenericAPIView for user details
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = self.get_serializer(user)
        
        # Check follow status
        is_following = request.user.is_following(user) if request.user.is_authenticated else False
        
        return Response({
            'user': serializer.data,
            'is_following': is_following,
            'can_follow': request.user != user
        })