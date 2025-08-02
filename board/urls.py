from django.urls import path

from board.views import TopicListView, TopicCreateView


app_name = 'topics'

urlpatterns = [
    path('', TopicListView.as_view(), name='list'),
    path('topics/add/', TopicCreateView.as_view(), name='topic_create'),
]
