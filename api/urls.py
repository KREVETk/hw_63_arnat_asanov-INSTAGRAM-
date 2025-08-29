from django.urls import path
from .views import (
    PostListCreateAPIView, PostDetailAPIView, ToggleLikeAPIView,
    CommentListCreateAPIView, CommentDetailAPIView
)

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', ToggleLikeAPIView.as_view(), name='post-toggle-like'),

    path('posts/<int:post_pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]
