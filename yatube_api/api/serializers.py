from rest_framework import serializers

from posts.models import Comment, Post, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
        )

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
        )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
