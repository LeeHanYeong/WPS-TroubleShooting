from io import BytesIO

import magic
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    img_profile_thumbnail = models.ImageField(upload_to='user', blank=True)

    def save(self, *args, **kwargs):
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
        super().save(*args, **kwargs)
