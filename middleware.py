from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import CsrfViewMiddleware

class CsrfExemptForOAuth(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.auth and hasattr(request.auth, 'token'):
            return None  # Bypass CSRF for OAuth requests
        return CsrfViewMiddleware().process_view(request, view_func, view_args, view_kwargs)