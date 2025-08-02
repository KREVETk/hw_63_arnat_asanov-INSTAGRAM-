from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import forms
from .forms.user import UserRegisterForm
from .forms.topic_form import TopicForm
from .models import Topic, Reply, User


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'board/register.html'
    success_url = reverse_lazy('board:login')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class TopicListView(ListView):
    model = Topic
    template_name = 'board/topics_list.html'
    context_object_name = 'topics'
    paginate_by = 5

    def get_queryset(self):
        return Topic.objects.order_by('-created_at')


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'board/topic_form.html'
    success_url = reverse_lazy('board:topic_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш ответ...'}),
        }


class TopicDetailView(FormMixin, DetailView):
    model = Topic
    template_name = 'board/topic_detail.html'
    context_object_name = 'topic'
    form_class = ReplyForm
    paginate_by = 8

    def get_success_url(self):
        return reverse('board:topic_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        replies_list = self.object.replies.all().order_by('created_at')
        paginator = Paginator(replies_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            replies = paginator.page(page)
        except PageNotAnInteger:
            replies = paginator.page(1)
        except EmptyPage:
            replies = paginator.page(paginator.num_pages)

        context['replies'] = replies
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('board:login')

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.topic = self.object
            reply.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'board/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_topics'] = Topic.objects.filter(author=self.request.user).order_by('-created_at')
        context['topics_count'] = context['user_topics'].count()
        context['posts_count'] = self.request.user.post_count()
        return context
