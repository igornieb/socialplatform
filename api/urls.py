from django.urls import path, include
from api.views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

urlpatterns = [
    path('', PostList.as_view()),
    path('register', UserRegister.as_view()),
    path('account-list', AccountList.as_view()),
    path('user/<pk>', account_detail),
    path('settings',AccountSettings.as_view()),
    path('account/follows/<pk>', FollowsList.as_view()),
    path('follow/<pk>', FollowAccount.as_view()),
    path('account/followers/<pk>', FollowerList.as_view()),
    path('post/<pk>', PostDetail.as_view()),
    path('post/comments/<pk>', PostCommentList.as_view()),
    path('comment/<pk>', CommentDetail.as_view()),
    path('post/likes/<pk>', LikePostList.as_view()),
    path('trending/posts/<int:days>', trending_posts),
    path('trending/users', trending_accounts),
    path('search/<str:query>', search_accounts),
    path('notifications', NotificationList.as_view()),
    path('api-auth', include('rest_framework.urls')),
    #path('api-token-auth', views.obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)
