from django.urls import path

from board.views import TopicListView, TopicCreateView


urlpatterns = [
    path('', TopicListView.as_view(), name='topic_list'),
    path('topics/add/', TopicCreateView.as_view(), name='topic_create'),
]
