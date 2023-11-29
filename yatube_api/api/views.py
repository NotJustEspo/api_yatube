from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from api.permissions import AuthorOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostsViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с постами.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, AuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Класс для работы с группами.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с комментами.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, AuthorOrReadOnly]

    def get_object_new(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        post = self.get_object_new()
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = self.get_object_new()
        serializer.save(author=self.request.user, post=post)
