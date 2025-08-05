from django.urls import path
from django.shortcuts import redirect
from django.views.generic import RedirectView

from board.views import (
    RegisterView, CustomLoginView, CustomLogoutView,
    ProfileUpdateView, UserDetailView,
    PostCreateView, PostDetailView, UserListView, PostListView, ToggleLikeView, ToggleFollowView, UserSearchView
)


app_name = 'board'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/search/', UserSearchView.as_view(), name='user_search'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('posts/add/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('post/<int:pk>/like/', ToggleLikeView.as_view(), name='post_like_toggle'),
    path('user/<int:pk>/follow/', ToggleFollowView.as_view(), name='user_follow_toggle'),

    path('accounts/login/', RedirectView.as_view(pattern_name='login', permanent=False))
]
