# blog/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Post
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from .models import Comment
from .forms import CommentForm, CommentUpdateForm
from django.db.models import Q
from django.shortcuts import render
from .models import Post, Tag



def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/profile.html', context)

# CRUD Views
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(is_active=True)
        return context

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post.pk}) + f'#comment-{comment.id}')
        else:
            messages.error(request, 'There was an error with your comment. Please try again.')
    
    return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post.pk}))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_pk']}) + f'#comment-{self.object.id}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk}) + f'#comment-{self.object.id}'

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.is_active = False  # Soft delete
        comment.save()
        messages.success(request, 'Your comment has been deleted successfully!')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'likes_count': comment.likes.count()})



def search_posts(request):
    query = request.GET.get('q', '')
    
    # Using Post.objects.filter for search functionality
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
    else:
        posts = Post.objects.all().order_by('-published_date')
    
    context = {
        'posts': posts,
        'query': query,
        'results_count': posts.count()
    }
    return render(request, 'blog/search_results.html', context)

def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.all()
    
    posts = Post.objects.filter(tags=tag).order_by('-published_date')


    context = {
        'tag': tag,
        'posts': posts,
        'results_count': posts.count()
    }
    return render(request, 'blog/posts_by_tag.html', context)

def posts_by_author(request, username):
    author = get_object_or_404(User, username=username)
    
    # Using Post.objects.filter to get posts by author
    posts = Post.objects.filter(author=author).order_by('-published_date')
    
    context = {
        'author': author,
        'posts': posts,
        'results_count': posts.count()
    }
    return render(request, 'blog/posts_by_author.html', context)

def latest_posts(request):
    # Using Post.objects.filter to get recent posts (last 7 days)
    from django.utils import timezone
    from datetime import timedelta
    
    one_week_ago = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(published_date__gte=one_week_ago).order_by('-published_date')
    
    context = {
        'posts': posts,
        'time_period': 'last 7 days'
    }
    return render(request, 'blog/latest_posts.html', context)

def popular_posts(request):
    # Using Post.objects.filter with annotation for popular posts (most comments)
    from django.db.models import Count
    
    posts = Post.objects.annotate(comment_count=Count('comments')).filter(comment_count__gt=0).order_by('-comment_count')[:10]
    
    context = {
        'posts': posts,
        'title': 'Most Discussed Posts'
    }
    return render(request, 'blog/popular_posts.html', context)

def posts_with_tag_count(request):
    # Using Post.objects.filter to demonstrate complex filtering
    # Get posts that have at least 2 tags and were published recently
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count
    
    one_month_ago = timezone.now() - timedelta(days=30)
    
    posts = Post.objects.filter(
        published_date__gte=one_month_ago
    ).annotate(
        tag_count=Count('tags')
    ).filter(
        tag_count__gte=2
    ).order_by('-published_date')
    
    context = {
        'posts': posts,
        'title': 'Recent Posts with Multiple Tags'
    }
    return render(request, 'blog/tagged_posts.html', context)

# Utility function using Post.objects.filter
def get_recent_posts(limit=5):
    """Utility function to get recent posts using Post.objects.filter"""
    return Post.objects.all().order_by('-published_date')[:limit]

def get_popular_tags(limit=10):
    """Utility function to get popular tags using Post.objects.filter and aggregation"""
    from django.db.models import Count
    return Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count')[:limit]

# Admin-style views using Post.objects.filter
@login_required
def my_posts(request):
    """View showing only the current user's posts using Post.objects.filter"""
    posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'posts': posts,
        'title': 'My Posts'
    }
    return render(request, 'blog/post_list.html', context)

@login_required
def draft_posts(request):
    """View showing draft posts (optional field would need to be added to model)"""
    # If you add a 'status' field to Post model, you could use:
    # posts = Post.objects.filter(author=request.user, status='draft').order_by('-created_date')
    posts = Post.objects.filter(author=request.user)  # Placeholder
    
    context = {
        'posts': posts,
        'title': 'My Drafts'
    }
    return render(request, 'blog/post_list.html', context)

# Advanced filtering examples
def advanced_search(request):
    """Advanced search with multiple filters using Post.objects.filter"""
    query = request.GET.get('q', '')
    tag_name = request.GET.get('tag', '')
    author_name = request.GET.get('author', '')
    
    # Start with all posts
    posts = Post.objects.all()
    
    # Apply filters based on query parameters
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    if tag_name:
        posts = posts.filter(tags__name__icontains=tag_name)
    
    if author_name:
        posts = posts.filter(author__username__icontains=author_name)
    
    # Order by publication date
    posts = posts.order_by('-published_date')
    
    context = {
        'posts': posts,
        'query': query,
        'tag_filter': tag_name,
        'author_filter': author_name,
        'results_count': posts.count()
    }
    return render(request, 'blog/advanced_search.html', context)