from django.contrib.auth import get_user_model
from django.db import models

MAX_TEXT_LENGTH_IN_STR = 30

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              blank=True, null=True)

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:MAX_TEXT_LENGTH_IN_STR]


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:MAX_TEXT_LENGTH_IN_STR]


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscribes')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='followers')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_subscribe',
                violation_error_message='Такая подписка уже существует!',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='following_is_not_user',
                violation_error_message=(
                    'Поля "user" и "following" должны различаться!'),
            ),
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.following.username}.'
