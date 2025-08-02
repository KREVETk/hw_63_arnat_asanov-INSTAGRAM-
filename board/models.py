from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'


class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path)

    def post_count(self):
        return self.replies.count()


class Topic(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User,
                on_delete=models.CASCADE,
                related_name='topics')
    created_at = models.DateTimeField(default=timezone.now)

    def reply_count(self):
        return self.replies.count()

    def __str__(self):
        return self.title


User = get_user_model()


class Reply(models.Model):
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ответ от {self.author} на тему "{self.topic.title}"'
