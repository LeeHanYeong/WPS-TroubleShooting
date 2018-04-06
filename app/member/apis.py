import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer, UserCreationSerializer

User = get_user_model()


class UserCreateAPIVIew(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer


class FacebookLoginView(APIView):
    def post(self, request):
        # 프론트로부터 전달된 token값
        token = request.data.get('token')
        if not token:
            raise APIException('token require')
        # 전달받은 token을 debug
        result = self.debug_token(token)
        # debug후 is_valid가 True일 경우
        if result['data']['is_valid']:
            # Facebook user id를 가져옴
            facebook_user_id = result['data']['user_id']
            # 해당 user id가 username인 유저가 있는지 검사
            if User.objects.filter(username=facebook_user_id).exists():
                user = User.objects.get(username=facebook_user_id)
                created = False
            else:
                user = User.objects.create_user(
                    username=facebook_user_id
                )
                created = True
            # user에 해당하는 Token을 가져오거나 새로 만듬
            token, _ = Token.objects.get_or_create(user=user)
            # 관련 정보들을 dict화
            ret = {
                'token': token.key,
                'user': UserSerializer(user).data,
                'user_created': created,
            }
            # API에서 돌려줌
            return Response(ret)
        else:
            raise APIException('token invalid')

    @staticmethod
    def debug_token(token):
        app_access_token = '{}|{}'.format(
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_SECRET_CODE,
        )
        url_debug_token = 'https://graph.facebook.com/debug_token'
        debug_token_params = {
            'input_token': token,
            'access_token': app_access_token
        }
        response = requests.get(url_debug_token, debug_token_params)
        result = response.json()
        return result
