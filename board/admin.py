from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Follow, Post, Comment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'avatar')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('avatar', 'bio', 'phone_number', 'gender')}),
    )
    search_fields = ('username', 'email')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    list_filter = ('created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'like_count', 'comment_count')
    search_fields = ('author__username', 'description')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('author__username', 'content', 'post__id')
    list_filter = ('created_at',)
