from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm , ProfileForm, CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after saving

    else:
        user_form = UserRegisterForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



class PostListView(ListView):
        model = Post
        template_name = 'blog/post_list.html'  # Template for displaying posts
        context_object_name = 'posts'
        ordering = ['-created_at']  # Show latest posts first
        paginate_by = 10
        def get_queryset(self):
            query = self.request.GET.get('q')  # Get the search query from the form

            if query:
                # Use Post.objects.filter directly to filter posts by title, content, or tags
                return Post.objects.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(tags__name__icontains=query)
                ).distinct()
            else:
                # If no query is provided, return all posts
                return Post.objects.all()

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Template for a single post
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'  # Template for creating a post
    fields = ['title', 'content']
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the post's author to the logged-in user
        return super().form_valid(form)
        

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'  # Reuse the form template for editing
    fields = ['title', 'content']
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Ensure only the post author can edit


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Template for confirming deletion
    success_url = reverse_lazy('post-list')  # Redirect after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Ensure only the author can delete
    


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # Create this template
    context_object_name = 'comment'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure the author remains the same
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only allow authors to edit
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'  # Create this template
    context_object_name = 'comment'

    def get_success_url(self):
        return self.object.post.get_absolute_url()  # Redirect to the post detail page

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only allow authors to delete

# blog/views.py

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    success_url = reverse_lazy('post-list')  # Redirect to the post list or another appropriate page

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    