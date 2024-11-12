# middleware.py
import threading

user_local = threading.local()


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_local.user = request.user
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_user():
        return getattr(user_local, 'user', None)
