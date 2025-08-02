from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms.user import UserRegisterForm
from .forms.topic_form import TopicForm
from .models import Topic


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class TopicListView(ListView):
    model = Topic
    template_name = 'forum/topics_list.html'
    context_object_name = 'topics'
    paginate_by = 5

    def get_queryset(self):
        return Topic.objects.order_by('-created_at')


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_form.html'
    success_url = reverse_lazy('topic_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
