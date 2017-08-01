from django.contrib import admin

from post.models import Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
