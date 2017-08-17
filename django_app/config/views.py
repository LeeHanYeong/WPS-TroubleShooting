from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class FrontView(View):
    def get(self, request):
        context = {
            'facebook_app_id': settings.FACEBOOK_APP_ID,
        }
        return render(request, 'front.html', context)


class FormFileView(TemplateView):
    template_name = 'form-file.html'
