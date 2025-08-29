from rest_framework import serializers
from board.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='like_count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'image', 'description', 'created_at', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at', 'likes_count']

