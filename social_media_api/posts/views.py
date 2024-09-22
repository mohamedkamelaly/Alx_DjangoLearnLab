from django.shortcuts import render
from .models import Comment , Post
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, permissions


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

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



