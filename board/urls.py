from django.urls import path

from board.views import TopicListView, TopicCreateView, TopicDetailView

app_name = 'topics'

urlpatterns = [
    path('', TopicListView.as_view(), name='list'),
    path('topics/add/', TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
]
