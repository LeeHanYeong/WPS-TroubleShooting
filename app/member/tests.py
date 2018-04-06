from rest_framework import status
from rest_framework.compat import authenticate
from rest_framework.test import APITestCase


class SignupTest(APITestCase):
    def tests_signup_django_user(self):
        username = 'TestUsername@abc.com'
        password = 'TestPassword'
        url = '/api/user-create/'
        data = {
            'email': username,
            'password1': password,
            'password2': password,
        }
        response = self.client.post(url, data)
        # Signup결과 response 테스트
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], username)
        self.assertEqual(response.data['email'], username)

        # authenticate를 사용해 실제 데이터베이스에 생성되었는지 확인,
        # 생성된 유저의 값을 테스트
        user = authenticate(username=username, password=password)
        self.assertEqual(response.data['pk'], user.pk)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)
