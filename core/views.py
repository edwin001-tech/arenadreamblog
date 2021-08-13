from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.db.models import Count, Q
import sys
from core.models import *
from core.forms import PostCreateForm

User = get_user_model()


# Create your views here.

#search blog

def search_blog(request):
    queryset = Post.objects.all()
    query = request.GET.get('search')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_blog.html', context)

context={}

@login_required
def search_users(request):
    if request.method == 'POST':
        kerko = request.POST.get('search')
        print(kerko)
        results = User.objects.filter(username__contains=kerko)
        global context
        context = {
            'results':results
        }
    return render(request, 'search_users.html', context)

def is_users(post_user, logged_user):
    return post_user == logged_user


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    form_class = PostCreateForm
    template_name = 'core/feed.html'
    context_object_name = 'all_posts'
    ordering = ['-created_on']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.values('user').annotate(author_count=Count('user')).order_by('-author_count')[:6]

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['user']).first())
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.followed)
        return Post.objects.filter(user__in=follows).order_by('-created_on')


class PostDetailView(View):
    template_name = 'core/post_detail.html'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            post_obj = Post.objects.get(pk=post_id)
            if self.request.user.is_authenticated:
                PostView.objects.get_or_create(
                    user=self.request.user,
                    post=post_obj
                )
        except Exception as e:
            return redirect(request.META.get('HTTP_REFERER'))

        try:
            Like.objects.get(user=request.user, post_id=post_id)
            liked_this_post = True
        except Exception as e:
            liked_this_post = False

        try:
            SavedPost.objects.get(user=request.user, post_id=post_id)
            post_saved = True
        except Exception as e:
            post_saved = False

        context = {
            'post': post_obj,
            'liked_this_post': liked_this_post,
            'post_saved': post_saved,
        }

        return render(request, self.template_name, context=context)

class PostCreateView(CreateView):
    model = Post
    template_name = 'core/post_new.html'
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a new post or article'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse("post_detail_view", kwargs={
            'id': form.instance.pk
        }))

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'core/post_new.html'
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update this post'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse("post_detail_view", kwargs={
            'id': form.instance.pk
        }))

class PostDeleteView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post_obj = Post.objects.get(pk=post_id)
        except Exception as e:
            pass
        if request.user == post_obj.user:
            post_obj.delete()

        return redirect(request.META.get('HTTP_REFERER'))


class PostSaveView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            post_obj = Post.objects.get(pk=post_id)
        except Exception as e:
            pass

        try:
            SavedPost.objects.create(post_id=post_id, user=self.request.user)
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))


class PostUnsaveView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            savedpost_obj = SavedPost.objects.get(post_id=post_id)
            savedpost_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))


class PostLikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            Like.objects.get(post_id=post_id, user=self.request.user)
        except Exception as e:
            Like.objects.create(post_id=post_id, user=self.request.user)

        return redirect(request.META.get('HTTP_REFERER'))


class PostUnlikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            like_obj = Like.objects.get(post_id=post_id, user=self.request.user)
            like_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))


class PostCommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        comment_text = request.POST.get('comment_text')

        Comment.objects.create(post_id=post_id, text=comment_text, user=self.request.user)

        return redirect(request.META.get('HTTP_REFERER'))


class FollowDoneView(View):
    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('followed_user_id'))

    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get('followed_user_id')
        followed_user_obj = User.objects.get(pk=followed_user_id)

        try:
            Follow.objects.get(user=request.user, followed=self.visible_user())
        except Exception as e:
            follow_obj = Follow.objects.create(user=request.user, followed=followed_user_obj)

        return redirect(request.META.get('HTTP_REFERER'))


class UnfollowDoneView(View):
    def post(self, request, *args, **kwargs):
        unfollowed_user_id = request.POST.get('unfollowed_user_id')
        unfollowed_user_obj = User.objects.get(pk=unfollowed_user_id)

        try:
            follow_obj = Follow.objects.get(user=self.request.user, followed=unfollowed_user_obj)
            follow_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))


class LikedPostsView(View):
    template_name = 'core/liked_posts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SavedPostsView(View):
    template_name = 'core/saved_posts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ExplorePostsView(View):
    template_name = 'core/posts_explore.html'

    def get(self, request, *args, **kwargs):
        all_posts = Post.objects.annotate(count=Count('like')).order_by('-count')
        context = {'all_posts': all_posts}
        return render(request, self.template_name, context=context)
