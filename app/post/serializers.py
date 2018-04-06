from rest_framework import serializers

from post.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    extra = serializers.SerializerMethodField('get_asdf')
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'title',
            'img_cover',
            'content',
            'tags',
            'created_date',

            'extra',
        )

    def get_asdf(self, obj):
        return self.context['extra']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    tag_names = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'img_cover',
            'content',
            'tags',
            'tag_names',
        )

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        tag_names = validated_data.get('tag_names')
        if tag_names and isinstance(tag_names, list):
            instance.tags.clear()
            for tag_name in tag_names:
                instance.tags.create(name=tag_name)
        return instance
