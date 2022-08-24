from django.conf import settings
from .views import session_writeout, autosave

class AutosaveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path_info != '/':
            autosave(minutes_between_saves=0.5)
        pass
        