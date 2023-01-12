from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from core.models import *
from core.utilis import create_action
from rest_framework.authtoken.models import Token
from datetime import datetime


def create_account(sender, instance, created, **kwargs):
    if created:
        new_user = Account.objects.create(user=instance)
        Token.objects.create(user=instance)


post_save.connect(create_account, sender=User)


def update_account(sender, instance, created, **kwargs):
    instance.account.save()
    print("Updated")


post_save.connect(update_account, sender=User)


def add_like(sender, instance, created, **kwargs):
    if created:
        instance.post.no_of_likes = instance.post.no_of_likes + 1
        create_action(instance.user, 'liked', instance, instance.post.owner)
        instance.post.save()


post_save.connect(add_like, sender=LikePost)


def del_like(sender, instance, **kwargs):
    instance.post.no_of_likes = instance.post.no_of_likes - 1
    instance.post.save()


pre_delete.connect(del_like, sender=LikePost)


def add_follower(sender, instance, created, **kwargs):
    if created:
        instance.follower.follows = instance.follower.follows + 1
        instance.followed.followers = instance.followed.followers + 1
        instance.follower.save()
        instance.followed.save()
        create_action(instance.follower, 'followed', instance, instance.followed)


post_save.connect(add_follower, sender=Follow)


def del_follower(sender, instance, **kwargs):
    instance.follower.follows = instance.follower.follows - 1
    instance.followed.followers = instance.followed.followers - 1
    instance.follower.save()
    instance.followed.save()


post_delete.connect(del_follower, sender=Follow)


def add_comment(sender, instance, created, **kwargs):
    if created:
        create_action(instance.owner, 'commented', instance, instance.post.owner)


post_save.connect(add_comment, sender=Comment)


def edit_post(sender, instance, **kwargs):
    instance.edit_date = datetime.now()
    instance.owner.save()


post_save.connect(edit_post, sender=Post)


def edit_comment(sender, instance, created, **kwargs):
    instance.edit_date = datetime.now()
    instance.owner.save()


post_save.connect(edit_comment, sender=Comment)
