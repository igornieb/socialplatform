from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.models import auth
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Post, Comment, Account, User, LikePost, Follow, Action
from core.forms import CommentForm, SearchForm, AccountForm, UserRegisterForm
import datetime

# TODO follow/unfollow (partialy done)

class PostList(ListView):
    def get(self, request):
        if request.user.is_authenticated:
            user_account = Account.objects.get(user=request.user)
            follow_list = Follow.objects.filter(follower=user_account)
            posts = Post.objects.filter(owner=user_account)
            if len(follow_list) == 0:
                posts |= get_popular_posts(50, 7)
                pass
            for follow in follow_list:
                tmp = Post.objects.filter(owner=follow.followed)
                posts |= tmp
            posts = posts.order_by('-date')
        else:
            posts = Post.objects.all().order_by('-owner__followers')

        paginator = Paginator(posts, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'posts': page_obj,
        }
        return render(request, 'index.html', context)

    template_name = 'index.html'


class PostDetail(DetailView):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-date')
        form = CommentForm
        paginator = Paginator(comments, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'posts': page_obj,
        }
        context = {'post': post,
                   'comments': page_obj,
                   'form': form,
                   }
        return render(request, 'post_detail.html', context)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['picture', 'description']
    template_name = 'add_post_form.html'
    extra_context = {'title': "Add new post"}

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner = Account.objects.get(user=self.request.user)
        post.save()
        return super(PostCreate, self).form_valid(form)

    def handle_no_permission(self):
        return redirect('login')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['description']
    template_name = 'edit_post_form.html'
    extra_context = {'title': "Edit post", }

    def get_object(self, **kwargs):
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
            user = Account.objects.get(user=self.request.user)
            if post.owner == user:
                return post
            else:
                raise Http404
        except:
            raise Http404

    def handle_no_permission(self):
        return redirect('login')

    def form_valid(self, form):
        if form.instance.owner.user == self.request.user:
            return super(PostUpdate, self).form_valid(form)
        else:
            return redirect('posts')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'Post'
    template_name = 'confirm_delete.html'
    extra_context = {'item': 'your post'}
    success_url = reverse_lazy('posts')

    def get_object(self, **kwargs):
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
            user = Account.objects.get(user=self.request.user)
            if post.owner == user:
                return post
            else:
                raise Http404
        except:
            raise Http404


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    extra_context = {'title': "Add new comment"}

    def form_valid(self, form):
        comment = form.save(commit=False)
        print(self.kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        comment.post = post
        comment.owner = Account.objects.get(user=self.request.user)
        comment.save()
        return super(CommentCreate, self).form_valid(form)

    def handle_no_permission(self):
        return redirect('login')


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "edit_comment_form.html"
    extra_context = {'title': "Edit comment"}

    def get_object(self, **kwargs):
        try:
            comment = Comment.objects.get(pk=self.kwargs['pk'])
            user = Account.objects.get(user=self.request.user)
            if comment.owner == user:
                return comment
            else:
                raise Http404
        except:
            raise Http404

    def handle_no_permission(self):
        return redirect('login')


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "confirm_delete.html"
    extra_context = {'item': 'your comment'}
    success_url = reverse_lazy('posts')

    def get_object(self, **kwargs):
        try:
            comment = Comment.objects.get(pk=self.kwargs['pk'])
            user = Account.objects.get(user=self.request.user)
            if comment.owner == user:
                return comment
            else:
                raise Http404
        except:
            raise Http404

    def handle_no_permission(self):
        return redirect('login')


class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        likes = LikePost.objects.filter(user=account)
        comments = Comment.objects.filter(owner=account)
        actions = Action.objects.filter(content_user=account)

        paginator = Paginator(actions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'account': account,
                   'likes': likes,
                   'comments': comments,
                   'actions': page_obj,
                   }

        return render(request, 'settings.html', context)

    def handle_no_permission(self):
        return redirect('login')


class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'edit_account_form.html'
    extra_context = {'title': "Account settings"}
    success_url = reverse_lazy('settings')

    def get_object(self):
        return Account.objects.get(user=self.request.user)

    def handle_no_permission(self):
        return redirect('login')


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = User
    context_object_name = 'account'
    extra_context = {'item':'your account'}
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('posts')

    def get_object(self):
        return self.request.user

    def handle_no_permission(self):
        return redirect('login')


def user_posts(request, pk):
    user_object = Account.objects.get(pk=pk)
    posts = Post.objects.filter(owner=user_object)
    paginator = Paginator(posts, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts': page_obj,
               'account': user_object,
               }
    if request.user.is_authenticated:
        if request.user.account.check_follow(user_object):
            context.update({'follow_action': 'Unfollow', })
        else:
            context.update({'follow_action': 'Follow', })
    return render(request, 'user_posts.html', context)


class AccountFollowersList(ListView):
    def get_object(self, pk):
        try:
            user = Account.objects.get(pk=pk)
            return Follow.objects.filter(followed=user)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        followers = self.get_object(pk)
        account = Account.objects.get(pk=pk)
        paginator = Paginator(followers, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'account': account,
                   'followers': page_obj,
                   }
        if request.user.is_authenticated:
            if request.user.account.check_follow(account):
                context.update({'follow_action': 'Unfollow', })
            else:
                context.update({'follow_action': 'Follow', })

        return render(request, 'user_followers.html', context)


class AccountFollowsList(ListView):
    def get_object(self, pk):
        try:
            user = Account.objects.get(pk=pk)
            return Follow.objects.filter(follower=user)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        followers = self.get_object(pk)
        account = Account.objects.get(pk=pk)
        paginator = Paginator(followers, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'account': account,
                   'followers': followers,
                   }
        if request.user.is_authenticated:
            if request.user.account.check_follow(account):
                context.update({'follow_action': 'Unfollow', })
            else:
                context.update({'follow_action': 'Follow', })

        return render(request, 'user_follows.html', context)


class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'edit_account_form.html'
    extra_context = {'title': "Account settings"}
    success_url = reverse_lazy('settings')

    def get_object(self):
        return Account.objects.get(user=self.request.user)

    def handle_no_permission(self):
        return redirect('login')


def get_popular_posts(no_of_posts, days):
    # most popular posts from past (7) days

    return Post.objects.filter(date__gte=(datetime.date.today() - datetime.timedelta(days=days))).order_by(
        '-no_of_likes')[:no_of_posts]


def get_popular_accounts(no_of_users, account_object):
    account_list = Account.objects.all().order_by('-followers')
    if account_object is not None:
        users = []
        for user in account_list:
            if account_object.check_follow(user) is False and user != account_object:
                users.append(user)
    else:
        users = account_list

    return users[:no_of_users]


class SearchView(View):
    def get(self, request):
        form = SearchForm
        if self.request.user.is_authenticated:
            account_object = Account.objects.get(user=self.request.user)
            popular_users = get_popular_accounts(60, account_object)
        else:
            popular_users = get_popular_accounts(8, None)
        popular_posts = get_popular_posts(80, 7)

        paginator = Paginator(popular_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': form,
            'popular_posts': page_obj,
            'popular_users': popular_users,
        }
        return render(request, 'search.html', context)

    def post(self, request):
        if len(request.POST['search']) < 3:
            return redirect('search')
        results = Account.objects.filter(user__username__icontains=request.POST['search'])
        form = SearchForm
        context = {
            'form': form,
            'results': results,
        }
        return render(request, 'search.html', context)


@login_required(login_url='login')
def follow(request, pk):
    follower = Account.objects.get(user=request.user)
    followed = Account.objects.get(pk=pk)
    if follower == followed:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if follower.check_follow(followed):
        Follow.objects.get(follower=follower, followed=followed).delete()
    else:
        Follow.objects.create(follower=follower, followed=followed)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def like_post(request, pk):
    user_object = Account.objects.get(user=request.user)
    post_object = Post.objects.get(pk=pk)
    if LikePost.objects.filter(user=user_object, post=post_object).exists():
        LikePost.objects.get(user=user_object, post=post_object).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        LikePost.objects.create(user=user_object, post=post_object)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SignUpView(CreateView):
    template_name = 'form_user.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')


def logout(request):
    auth.logout(request)
    return redirect('posts')
