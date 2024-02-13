from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'upvotes', 'downvotes', )

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'created_at', 'upvotes', 'downvotes', 'is_authenticated_only', 'comments', )

    def to_representation(self, instance):
        """
        Customize the serialized representation based on user authentication status.
        """
        print(self.context)
        user = self.context['request'].user
        data = super().to_representation(instance)

        if user.is_authenticated or not instance.is_authenticated_only:
            return data
        else:
            # If the user is not authenticated and the post is for authenticated users only,
            # you may choose to customize the output or exclude the post altogether.
            return None
        
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'upvotes', 'downvotes')