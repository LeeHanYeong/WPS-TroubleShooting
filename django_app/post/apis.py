from rest_framework import viewsets, generics
from rest_framework.response import Response

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
        print(request.data)
        print(args)
        print(kwargs)
        return super().create(request, *args, **kwargs)


# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
