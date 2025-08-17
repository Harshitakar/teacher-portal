from django.utils.deprecation import MiddlewareMixin
from .models import Teacher
import secrets

SESSIONS = {} 
CSRF_TOKENS = {}

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.teacher = None
        token = request.COOKIES.get("session_token")
        if token and token in SESSIONS:
            try:
                request.teacher = Teacher.objects.get(id=SESSIONS[token])
            except Teacher.DoesNotExist:
                request.teacher = None

    def process_response(self, request, response):
        sess_token = request.COOKIES.get("session_token")
        if sess_token and sess_token in SESSIONS:
            if sess_token not in CSRF_TOKENS:
                CSRF_TOKENS[sess_token] = secrets.token_urlsafe(32)
            response.set_cookie(
                "csrf_token",
                CSRF_TOKENS[sess_token],
                httponly=False,
                secure=False,
                samesite="Strict",
            )
        return response
