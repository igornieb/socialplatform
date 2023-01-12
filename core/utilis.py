from django.contrib.contenttypes.models import ContentType
from core.models import Action
import datetime
from django.utils import timezone


def create_action(user, verb, object, content_user=None):
    action = Action(user=user, verb=verb, content_object=object, content_user=content_user)
    action.save()
    return True