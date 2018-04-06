from io import BytesIO

import magic
from PIL import Image
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models


class UserManager(DjangoUserManager):
    def create_django_user(self, *args, **kwargs):
        return super().create_user(*args, **kwargs)

    def create_facebook_user(self, *args, **kwargs):
        pass

    def create_google_user(self, *args, **kwargs):
        pass


class User(AbstractUser):
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_GOOGLE = 'g'
    CHOICES_USER_TYPE = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_GOOGLE, 'Google'),
    )
    user_type = models.CharField(max_length=1, choices=CHOICES_USER_TYPE, default=USER_TYPE_DJANGO)
    img_profile = models.ImageField(upload_to='user', blank=True)
    img_profile_thumbnail = models.ImageField(upload_to='user', blank=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        self._save_thumbnail_process()
        super().save(*args, **kwargs)

    def _save_thumbnail_process(self):
        """
        save() 메서드 실행 도중 img_profile필드의 썸네일 생성에 관한 로직
        :return:
        """
        if self.img_profile:
            # 이미지파일의 이름과 확장자를 가져옴
            full_name = self.img_profile.name.rsplit('/')[-1]
            full_name_split = full_name.rsplit('.', maxsplit=1)

            temp_file = BytesIO()
            temp_file.write(self.img_profile.read())
            temp_file.seek(0)
            mime_info = magic.from_buffer(temp_file.read(), mime=True)
            temp_file.seek(0)

            name = full_name_split[0]
            ext = mime_info.split('/')[-1]

            # Pillow를 사용해 이미지 파일 로드
            im = Image.open(self.img_profile)
            # 썸네일 형태로 데이터 변경
            im.thumbnail((200, 200))

            # 썸네일 이미지 데이터를 가지고 있을 임시 메모리 파일 생성
            temp_file = BytesIO()
            # 임시 메모리 파일에 Pillow인스턴스의 내용을 기록
            im.save(temp_file, ext)
            # 임시 메모리파일을 Django의 File로 한번 감싸 썸네일 필드에 저장
            self.img_profile_thumbnail.save(f'{name}_thumbnail.{ext}', File(temp_file), save=False)
        else:
            self.img_profile_thumbnail.delete(save=False)
