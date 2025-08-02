from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Topic, Reply


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'avatar')
    fieldsets = BaseUserAdmin.fieldsets + ((None, {'fields': ('avatar',)}),)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'reply_count')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content', 'author__username')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'topic__title')
