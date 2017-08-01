from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    # img_cover = serializers.ImageField(use_url=True)

    class Meta:
        model = Post
        fields = '__all__'
