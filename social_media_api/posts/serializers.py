from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name')

class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        source='author',
        write_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_id', 'content', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        source='author',
        write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'author_id', 'title', 'content',
                 'created_at', 'updated_at', 'like_count', 'comment_count',
                 'comments', 'is_liked', 'likes')
        read_only_fields = ('id', 'created_at', 'updated_at', 'likes')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content')