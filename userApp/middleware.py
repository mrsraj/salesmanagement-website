from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect


class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def stats(self, os_info):
        print("abcd")

    def __call__(self, request):
        if "admin" not in request.path:
            self.stats(request.META["HTTP_USER_AGENT"])

        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if "pswdverify" not in request.path:
            print(request.path)
            return HttpResponse("/")

        return None
