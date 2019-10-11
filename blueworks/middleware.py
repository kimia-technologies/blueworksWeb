import re

from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout


class RbacMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return redirect('sites.html')

        # if path == reverse('accounts:logout').lstrip('/'):
        #     logout(request)

        # if request.user.is_authenticated() and url_is_exempt:
        #     return redirect(settings.LOGIN_REDIRECT_URL)
        # elif request.user.is_authenticated() or url_is_exempt:
        #     return None
        # else:
        #     return redirect(settings.LOGIN_URL)

        # regex_http_ = re.compile(r'^HTTP_.+$')
        # regex_content_type = re.compile(r'^CONTENT_TYPE$')
        # regex_content_length = re.compile(r'^CONTENT_LENGTH$')

        # self.request_headers = {}
        # for header in request.META:
        #     if regex_http_.match(header) or regex_content_type.match(header) or regex_content_length.match(header):
        #         self.request_headers[header] = request.META[header]
