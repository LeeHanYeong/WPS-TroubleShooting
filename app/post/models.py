from django.db import models
from django.utils import timezone

from utils.fields import CustomImageField


class Post(models.Model):
    title = models.CharField(max_length=100)
    img_cover = CustomImageField(upload_to='post', blank=True,
                                 default_static_image='images/no_image.png')
    content = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
