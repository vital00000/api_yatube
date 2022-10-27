from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def __get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.__get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.__get_post())
