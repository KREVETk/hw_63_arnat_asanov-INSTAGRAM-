from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, IntegerField, Case, When
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View
from django.views.generic.edit import FormMixin

from .forms.register_form import RegisterForm
from .models import Post, Comment, Follow
from .forms.profile_update_form import ProfileUpdateForm
from .forms.post_create_form import PostCreateForm
from .forms.comment_form import CommentForm
from .mixins import RedirectBackMixin

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'board/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query)
            ).distinct()
        return User.objects.all()


class UserDetailView(DetailView):
    model = User
    template_name = 'board/user_detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()

        posts_qs = Post.objects.filter(author=profile_user).order_by('-created_at')
        paginator = Paginator(posts_qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        posts_page = paginator.get_page(page_number)

        comments = Comment.objects.filter(author=profile_user).order_by('-created_at')

        context['posts_paginator'] = posts_page
        context['comments'] = comments
        context['posts_count'] = posts_qs.count()
        context['followers_count'] = profile_user.followers.count()
        context['following_count'] = profile_user.following.count()

        context['is_own_profile'] = self.request.user == profile_user

        if self.request.user.is_authenticated and not context['is_own_profile']:
            context['is_following'] = Follow.objects.filter(follower=self.request.user, following=profile_user).exists()
        else:
            context['is_following'] = False

        return context


class RegisterView(RedirectBackMixin, CreateView):
    form_class = RegisterForm
    template_name = 'board/register.html'
    success_url = reverse_lazy('board:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next') or self.request.POST.get('next') or ''
        context['next'] = next_url
        return context


class ProfileUpdateView(RedirectBackMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'board/profile_edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.get_redirect_url() or reverse('board:user_detail', kwargs={'username': self.request.user.username})


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        return Post.objects.select_related('author').order_by('-created_at')


class CustomLoginView(LoginView):
    template_name = 'board/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next') or self.request.POST.get('next') or ''
        context['next'] = next_url
        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('board:login')


class HomeFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'board/post_feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        following = Follow.objects.filter(follower=self.request.user).values_list('following', flat=True)
        return Post.objects.filter(author__in=following).order_by('-created_at')


class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'board/feed.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        following_users_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)

        return Post.objects.annotate(
            is_following=Case(
                When(author__in=following_users_ids, then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-is_following', '-created_at')


class PostCreateView(RedirectBackMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'board/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse('board:post_list')


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    paginate_comments_by = 5

    def get_success_url(self):
        return reverse('board:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        author = self.object.author

        context['is_following'] = author.followers.filter(follower=user).exists() if user.is_authenticated else False
        context['form'] = self.get_form()

        comments_list = self.object.comments.select_related('author').order_by('created_at')
        paginator = Paginator(comments_list, self.paginate_comments_by)
        page_number = self.request.GET.get('page')
        comments = paginator.get_page(page_number)
        context['comments'] = comments

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('board:login')

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)


class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        next_url = request.POST.get('next') or reverse('board:post_list')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'liked': liked, 'likes_count': post.like_count()})
        else:
            return redirect(next_url)


class ToggleFollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        target_user = get_object_or_404(User, pk=pk)

        if request.user == target_user:
            return redirect('board:user_detail', username=target_user.username)

        follow_relation = Follow.objects.filter(follower=request.user, following=target_user).first()

        if follow_relation:
            follow_relation.delete()
            action = 'unfollowed'
        else:
            Follow.objects.create(follower=request.user, following=target_user)
            action = 'followed'

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok', 'action': action})

        return redirect('board:user_detail', username=target_user.username)


class UserSearchView(ListView):
    model = User
    template_name = 'board/user_search_results.html'
    context_object_name = 'users'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query)
            ).distinct()
        return User.objects.none()
