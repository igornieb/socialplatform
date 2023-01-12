from django.urls import path
from django.contrib.auth.views import LoginView, PasswordChangeView
from core.views import *

urlpatterns = [
    path("", PostList.as_view(), name='posts'),
    path("post/<str:pk>", PostDetail.as_view(), name='post'),
    path("post-create", PostCreate.as_view(), name='post-create'),
    path("post-update/<str:pk>", PostUpdate.as_view(), name='post-update'),
    path("post-delete/<str:pk>", PostDelete.as_view(), name='post-delete'),
    path("post-comment/<str:pk>", CommentCreate.as_view(), name='add-comment'),
    path("comment-update/<str:pk>", CommentUpdate.as_view(), name='comment-update'),
    path("comment-delete/<str:pk>", CommentDelete.as_view(), name='comment-delete'),
    path("like/<str:pk>", like_post, name='like'),
    path("follow/<str:pk>", follow, name="follow"),
    path("user/<str:pk>", user_posts, name='user'),
    path("user/followers/<str:pk>", AccountFollowersList.as_view(), name="followers"),
    path("user/follows/<str:pk>", AccountFollowsList.as_view(), name="follows"),
    path("settings", AccountView.as_view(), name='settings'),
    path("settings/delete", AccountDelete.as_view(), name='account-delete'),
    path("search", SearchView.as_view(), name="search"),
    path("settings/update", AccountUpdate.as_view(), name='account-update'),
    path("settings/delete", AccountDelete.as_view(), name='account-delete'),
    path("settings/change-password",PasswordChangeView.as_view(template_name='change_password.html',success_url=reverse_lazy('logout'), extra_context={'title': 'Change password', }),name="change-password"),
    path("register", SignUpView.as_view(extra_context={'title': "Register", }), name='register'),
    path("login", LoginView.as_view(template_name='form_login.html',extra_context={'title': 'Login',}), name='login'),  # edit
    path("logout", logout, name='logout'),
]
