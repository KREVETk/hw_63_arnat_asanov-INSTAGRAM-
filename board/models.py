from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.username}/{filename}'


def post_image_path(instance, filename):
    return f'posts/user_{instance.author.username}/{filename}'


class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другое'),
    ], blank=True)

    def post_count(self):
        return self.posts.count()

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def liked_posts_count(self):
        return self.liked_posts.count()

    def is_following(self, other_user):
        return self.following.filter(following=other_user).exists()

    def is_followed_by(self, user):
        if not user.is_authenticated:
            return False
        return self.followers.filter(follower=user).exists()

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} → {self.following}'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to=post_image_path)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(pk=user.pk).exists()
        return False

    def __str__(self):
        return f'Пост от {self.author.username} ({self.created_at.strftime("%d.%m.%Y")})'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author.username} к посту {self.post.id}'
