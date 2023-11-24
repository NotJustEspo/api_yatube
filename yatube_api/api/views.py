from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, viewsets
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError('Изменение чужого контента запрещено!')
        super(PostsViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError('Удаление чужого контента запрещено!')
        super(PostsViewSet, self).perform_destroy(instance)


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer

#     def get_queryset(self):
#         post_id = self.kwsrgs.get('post_id')
#         new_queryset = Comment.objects.filter(post=post_id)
#         return new_queryset


# @api_view(['GET'])
# def api_group(request):
#     groups = Group.objects.all()
#     serializer = GroupSerializer(groups, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def api_group_detail(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     serializer = GroupSerializer(group)
#     return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def api_posts(request):
#     if request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     posts = Post.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def api_posts_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     user = request.user
#     if user != post.author:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#     if request.method == 'PUT' or request.method == 'PATCH':
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
