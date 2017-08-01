from rest_framework import viewsets

from post.models import Post, Tag
from post.serializers import PostSerializer, TagSerializer, PostUpdateSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        return PostSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
