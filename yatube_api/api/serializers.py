from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .fields import Base64ImageField
from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого автора!',
            )
        ]

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return value
