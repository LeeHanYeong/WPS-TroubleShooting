"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from post.apis import PostViewSet, TagViewSet, PostDetailView
from member.apis import FacebookLoginView, DjangoUserCreateView

from . import views

router = DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'tag', TagViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/facebook-login/', FacebookLoginView.as_view()),
    url(r'^api/user-create/', DjangoUserCreateView.as_view()),
    url(r'^$', views.FrontView.as_view()),
    url(r'^form-file/', views.FormFileView.as_view()),
    url(r'^post-detail/(?P<pk>\d+)/', PostDetailView.as_view()),
]
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
)
