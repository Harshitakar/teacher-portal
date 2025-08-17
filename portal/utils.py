import os, hmac, hashlib, secrets
from functools import wraps
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .middleware import SESSIONS, CSRF_TOKENS

ITERATIONS = 100_000

def hash_password(raw_password: str, salt_hex: str | None = None):
    salt = os.urandom(32) if salt_hex is None else bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", raw_password.encode(), salt, ITERATIONS)
    return salt.hex(), dk.hex()

def verify_password(raw_password: str, salt_hex: str, hash_hex: str):
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", raw_password.encode(), salt, ITERATIONS)
    return hmac.compare_digest(dk.hex(), hash_hex)

def require_login(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not getattr(request, "teacher", None):
            if request.headers.get("Accept", "").find("text/html") != -1 and request.method == "GET":
                return redirect("login")
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return view(request, *args, **kwargs)
    return wrapper

def require_csrf(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            token = request.headers.get("X-CSRFToken") or request.POST.get("csrf_token")
            sess_token = request.COOKIES.get("session_token")
            if not token or not sess_token or CSRF_TOKENS.get(sess_token) != token:
                return JsonResponse({"error": "CSRF validation failed"}, status=403)
        return view(request, *args, **kwargs)
    return wrapper

def calculate_new_marks(existing: int, new: int) -> int:
    """Assignment rule: when same (name, subject) exists, increase marks using helper logic."""
    return existing + new  # simple sum per PDF; business rule can be adjusted.
