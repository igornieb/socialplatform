from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import uuid

User = get_user_model()


class Account(models.Model):
    def __str__(self):
        return self.user.username

    def user_media_path(self, filename):
        return 'media/user_{0}/profile/{1}'.format(self.user.pk, filename)

    def get_absolute_url(self):
        return reverse("user", kwargs={'pk': self.pk})

    def check_follow(self, account_object):
        if Follow.objects.filter(follower=self, followed=account_object).exists():
            return True
        else:
            return False
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_media_path, default='media/blank.png')
    name = models.CharField(max_length=100, default="")
    bio = models.TextField()
    followers = models.IntegerField(default=0)
    follows = models.IntegerField(default=0)


class Action(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    verb = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now())
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    content_user = models.ForeignKey(Account, related_name="content_user", on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)


class Post(models.Model):
    def __str__(self):
        return "post by " + self.owner.user.username

    def post_media_path(self, filename):
        return 'media/user_{0}/posts/{1}'.format(self.owner.pk, filename)

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})
        # return "/post/%i" % self.pk

    def get_newest_comment(self):
        if Comment.objects.filter(post=self).exists():
            comment = Comment.objects.filter(post=self).order_by('-date').first()
            return comment

    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=post_media_path)
    description = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    edit_date = models.DateTimeField(default=datetime.now())
    no_of_likes = models.IntegerField(default=0)
    newest_comment = get_newest_comment
    action = GenericRelation(Action, related_query_name='post')

    class Meta:
        ordering = ('-date',)


class LikePost(models.Model):
    def __str__(self):
        return "post by " + self.post.owner.user.username

    def get_absolute_url(self):
        return self.post.get_absolute_url()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    action = GenericRelation(Action, related_query_name='like')


class Follow(models.Model):
    def __str__(self):
        return self.followed.user.username

    def get_absolute_url(self):
        return reverse("user", kwargs={'pk': self.followed.pk})

    follower = models.ForeignKey(Account, related_name="follower", on_delete=models.CASCADE)
    followed = models.ForeignKey(Account, related_name="followed", on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    action = GenericRelation(Action, related_query_name='follow')


class Comment(models.Model):
    def get_absolute_url(self):
        return reverse("post", kwargs={'pk': self.post.pk})
        # return "/post/%i" % self.post.pk

    def __str__(self):
        return "post by " + self.post.owner.user.username

    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    action = GenericRelation(Action, related_query_name='comment')
    edit_date = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ('-date',)
