from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from posts.models import Post, Group
from .serializers import CommentSerializer, PostSerializer, GroupSerializer


class IsAuthorPermission(permissions.BasePermission):
    """
    Пользовательское разрешение.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostsViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с постами.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorPermission]

    def perform_create(self, serializer):
        """
        Переопределение метода при создании поста.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Переопределение метода для обновления поста.
        """
        try:
            serializer.instance.author = self.request.user
            super().perform_update(serializer)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        """
        Переопределение метода для удаления поста.
        """
        try:
            instance.author = self.request.user
            super().perform_destroy(instance)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)


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
    permission_classes = [permissions.IsAuthenticated, IsAuthorPermission]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        """
        Переопределение метода создания комментов.
        """
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """
        Переопределение метода обновления коммента.
        """
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        try:
            serializer.instance.author = self.request.user
            post = post
            super().perform_update(serializer)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        """
        Переопределение метода удаления коммента.
        """
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        try:
            instance.author = self.request.user
            post = post
            super().perform_destroy(instance)
        except PermissionError:
            raise Response(status=status.HTTP_403_FORBIDDEN)
