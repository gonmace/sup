# middleware.py
from threading import local

request_local = local()


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_local.request = request
        response = self.get_response(request)
        del request_local.request
        return response

    @staticmethod
    def get_request():
        return getattr(request_local, 'request', None)
