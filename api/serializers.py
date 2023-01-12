from rest_framework import serializers
from core.models import Account, Post, Comment, LikePost, Follow, Action
from django.contrib.auth import get_user_model
from core.forms import *
from django.contrib.auth import authenticate
from generic_relations.relations import GenericRelatedField
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   email=validated_data['email'])
        user.set_password(validated_data['password1'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AccountSerializer(serializers.ModelSerializer):
    user = User
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = Account
        fields = ['pk', 'username', 'profile_picture', 'name', 'bio', 'followers', 'follows']

    def update(self, instance, validated_data):
        instance.profile_picture=validated_data.get('profile_picture',instance.profile_picture)
        instance.name=validated_data.get('name',instance.name)
        instance.bio=validated_data.get('bio',instance.bio)
        instance.save()
        return instance

class ListPostSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(many=False, read_only=True)
    picture = serializers.ImageField()

    class Meta:
        model = Post
        fields = ['pk','owner', 'description', 'picture', 'date', 'no_of_likes']


class CommentSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(many=False, read_only=True)
    post = ListPostSerializer(many=False, read_only=True)
    comment_pk = serializers.IntegerField(source='pk', required=False)

    class Meta:
        model = Comment
        fields = ['comment_pk', 'owner', 'post', 'comment', 'date']

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class DetailPostSerializer(serializers.ModelSerializer):
    post_url = serializers.CharField(source='get_absolute_url')
    owner = AccountSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['post_url', 'owner', 'picture', 'description', 'date', 'no_of_likes', 'comments']

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class LikePostSerializer(serializers.ModelSerializer):
    user = AccountSerializer(many=False, read_only=True)
    post = DetailPostSerializer(many=False, read_only=True)

    class Meta:
        model = LikePost
        fields = ['user', 'post']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(source='follower.user')
    follower_url = serializers.CharField(source='follower.get_absolute_url')
    followed = serializers.CharField(source='followed.user')
    followed_url = serializers.CharField(source='followed.get_absolute_url')

    class Meta:
        model = LikePost
        fields = ['follower', 'follower_url', 'followed', 'followed_url']


class TargetRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Post):
            return value
        elif isinstance(value, LikePost):
            return value
        raise Exception('Unexpected type of tagged object')


class ActionSerializer(serializers.ModelSerializer):
    user = AccountSerializer(many=False, read_only=True)
    content_user=user = AccountSerializer(many=False, read_only=True)
    content_object = GenericRelatedField({
        Post: ListPostSerializer(),
        Comment: CommentSerializer(),
        LikePost: LikePostSerializer(),
        Account: AccountSerializer(),
        Follow: FollowSerializer(),
    })

    class Meta:
        model = Action
        fields = ['user', 'verb', 'content_object', 'content_user']
