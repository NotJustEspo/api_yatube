from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, viewsets
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        try:
            serializer.instance.author = self.request.user
            super(PostsViewSet, self).perform_update(serializer)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        try:
            instance.author = self.request.user
            super(PostsViewSet, self).perform_destroy(instance)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        try:
            serializer.instance.author = self.request.user
            post = post
            super(CommentViewSet, self).perform_update(serializer)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        try:
            instance.author = self.request.user
            post = post
            super(CommentViewSet, self).perform_destroy(instance)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)
