from django.contrib import admin
from core.models import Account, Post, Comment, LikePost, Follow, Action


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('owner', 'pk')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'comment')


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'content_object', 'date')
    list_filter = ('date',)
    search_fields = ('verb',)
