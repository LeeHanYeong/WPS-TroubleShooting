from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField()
    img_profile = serializers.ImageField()

    def create(self, validated_data):
        username = validated_data.get('username')
        img_profile = validated_data.get('img_profile')
        return User.objects.create(username=username, img_profile=img_profile)
