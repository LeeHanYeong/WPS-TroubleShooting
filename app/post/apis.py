from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, Tag
from post.serializers import PostSerializer, TagSerializer, PostUpdateSerializer, \
    PostCreateSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        elif self.action in ['create']:
            return PostCreateSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PostDetailView(APIView):
    """
    희진님 ModelSerializer의 extra data출력
    PostSerializer를 참조
    """
    serializer_class = PostSerializer

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = self.serializer_class(instance=post, context={'extra': 'context-extra'})
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
