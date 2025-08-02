from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from board.views import TopicListView, TopicCreateView, TopicDetailView, RegisterView

app_name = 'board'

urlpatterns = [
    path('', TopicListView.as_view(), name='list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='board/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='board:login'), name='logout'),
    path('topics/add/', TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
]
