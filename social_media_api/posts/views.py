from django.shortcuts import render
from .models import Comment , Post, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework import generics, permissions 
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')  # Filter by title
    content = filters.CharFilter(lookup_expr='icontains')  # Filter by content

    class Meta:
        model = Post
        fields = ['title', 'content']


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        # Check if the user is the author of the post
        if post.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user is the author of the post
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        comment = self.get_object()
        # Check if the user is the author of the comment
        if comment.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user is the author of the comment
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()

class LikePostView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['post_id'])
        user = request.user

        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'message': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the Like object
        like = Like.objects.create(user=user, post=post)

        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            target=post,
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id
        )

        return Response({'message': 'Post liked successfully!'}, status=status.HTTP_200_OK)

class UnlikePostView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['post_id'])
        user = request.user

        # Check if the user has liked the post
        like = Like.objects.filter(user=user, post=post).first()
        if like:
            like.delete()
            return Response({'message': 'Post unliked successfully!'}, status=status.HTTP_200_OK)

        return Response({'message': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)