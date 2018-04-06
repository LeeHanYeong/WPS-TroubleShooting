from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# class UserCreationSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     img_profile = serializers.ImageField()
#
#     def create(self, validated_data):
#         username = validated_data.get('username')
#         img_profile = validated_data.get('img_profile')
#         return User.objects.create(username=username, img_profile=img_profile)


class DjangoUserCreationSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'password1',
            'password2',
            'img_profile',
        )

    def validate_email(self, value):
        """
        ModelSerializer를 사용해서 이메일 필드의 validator를 자동으로 구현
        username이 주어진 값과 같은 유저가 이미 있으면 예외발생
        :param value:
        :return:
        """
        if self.Meta.model.objects.filter(username=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, attrs):
        """
        password1, password2가 같은지 비교 후
        username, password값을 설정 및 password1, password2 항목 삭제
        :param attrs:
        :return:
        """
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('Password not equal')
        attrs['username'] = attrs['email']
        attrs['password'] = attrs['password1']
        attrs.pop('password1')
        attrs.pop('password2')
        return attrs

    def create(self, validated_data):
        return self.Meta.model.objects.create_django_user(**validated_data)
