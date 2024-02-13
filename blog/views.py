from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .models import Comment

from .serializers import PostSerializer
from .serializers import CommentSerializer
from .serializers import PostListSerializer

@api_view(['GET'])
def post_all(request):

    post = Post.objects.all()
    serializer = PostListSerializer(post, many=True)

    response = {
        "status" : "success",
        "message": "all posts",
        "data"   : serializer.data
    }

    return Response(response)


@api_view(['GET'])
def post_detail(request, post_id):

    post = Post.objects.get(id=post_id)
    serializer = PostListSerializer(post)

    response = {
        "status" : "success",
        "message": "post",
        "data"   : serializer.data
    }
    
    return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):

    serializer = PostSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save(author=request.user)
        response = {
            "status"  : "success",
            "message" : "post created successfully",
            "data"    : serializer.data 
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    response = {
        "status"  : "error",
        "message" : "something is wrong :(",
        "data"    : {}
    }

    return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.upvote()
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.downvote()
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.upvote()
    serializer = CommentSerializer(comment)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.downvote()
    serializer = CommentSerializer(comment)
    return Response(serializer.data)