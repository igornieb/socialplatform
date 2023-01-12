from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import *
from core.views import get_popular_posts, get_popular_accounts
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly


class AccountList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class UserRegister(CreateAPIView):
    serializer_class = UserRegisterSerializer


@api_view(['GET'])
def account_detail(request, pk):
    # get object
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data)


class AccountSettings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = Account.objects.get(user=self.request.user)
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data)

    def patch(self, request):
        try:
            account = Account.objects.get(user=self.request.user)
            serializer = AccountSerializer(account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostList(APIView):
    def get(self, request):
        if self.request.user.is_authenticated:
            user_account = Account.objects.get(user=request.user)
            follow_list = Follow.objects.filter(follower=user_account)
            posts = Post.objects.filter(owner=user_account)
            if len(follow_list) == 0:
                posts |= get_popular_posts(50, 7)
            for follow in follow_list:
                tmp = Post.objects.filter(owner=follow.followed)
                posts |= tmp
            posts = posts.order_by('-date')
        else:
            posts = Post.objects.all().order_by('-owner__followers')
        serializer = ListPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = ListPostSerializer(data=request.data)
            owner = Account.objects.get(user=request.user)
            if serializer.is_valid():
                serializer.save(owner=owner)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowAccount(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Account.objects.get(pk=self.kwargs['pk'])
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        account = Account.objects.get(user=self.request.user)
        a = self.get_object()
        if account == a:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(follower=account, followed=a).exists():
            Follow.objects.get(follower=account, followed=a).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            Follow.objects.create(follower=account, followed=a).save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = DetailPostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, pk):
        post = self.get_object(pk)
        serializer = DetailPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid() and request.user == post.owner.user:
            serializer.save(owner=request.user.account)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.owner.user == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class NotificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        try:
            account = Account.objects.get(user=user)
            return Action.objects.filter(content_user=account).order_by('-date')
        except Account.DoesNotExist:
            raise Http404

    def get(self, request):
        if request.user.is_authenticated:
            actions = self.get_object(request.user)
            serializer = ActionSerializer(actions, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PostCommentList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.filter(post=Post.objects.get(pk=pk))
            # return Comment.objects.all()
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comments = self.get_object(pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        if request.user.is_authenticated:
            serializer = CommentSerializer(data=request.data)
            # THIS SHIT IS IMPORTANT (THINK SO)
            owner = Account.objects.get(user=request.user)
            post = Post.objects.get(pk=pk)
            ###
            if serializer.is_valid():
                #
                serializer.save(owner=owner, post=post)
                #
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)

    def patch(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid() and comment.owner.user == request.user:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        print(request.user)
        comment = self.get_object(pk)
        if comment.owner.user == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class LikePostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, post_pk):
        try:
            post = Post.objects.get(pk=post_pk)
            return LikePost.objects.filter(post=post)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        likes = self.get_object(pk)
        serializer = LikePostSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        # this serves as delete too
        if request.user.is_authenticated:
            likes = self.get_object(pk)
            serializer = LikePostSerializer(data=request.data)
            user = Account.objects.get(user=request.user)
            post = Post.objects.get(pk=pk)
            if likes.filter(user=user).exists():
                likes.get(user=user).delete()
                return Response(status=status.HTTP_200_OK)
            if serializer.is_valid():
                serializer.save(user=user, post=post)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowerList(APIView):
    def get_object(self, user_pk):
        try:
            user = Account.objects.get(pk=user_pk)
            return Follow.objects.filter(followed=user)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        followers = self.get_object(pk)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)


class FollowsList(APIView):
    def get_object(self, user_pk):
        try:
            user = Account.objects.get(pk=user_pk)
            return Follow.objects.filter(follower=user)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        followers = self.get_object(pk)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def trending_posts(request, days):
    # get object
    posts = get_popular_posts(50, days)
    serializer = ListPostSerializer(posts, many=True)
    if request.method == 'GET':
        return Response(serializer.data)
    return Http404


@api_view(['GET'])
def search_accounts(request, query):
    results = Account.objects.filter(user__username__icontains=query)
    serializer = AccountSerializer(results, many=True)
    if request.method == 'GET':
        return Response(serializer.data)
    return Http404


@api_view(['GET'])
def trending_accounts(request):
    # get object
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        accounts = get_popular_accounts(50, account)
    else:
        accounts = get_popular_accounts(50, None)
    serializer = AccountSerializer(accounts, many=True)
    if request.method == 'GET':
        return Response(serializer.data)
    return Http404
