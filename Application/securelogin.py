from django.conf import settings
from django.contrib.auth import get_user
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.sessions.middleware import SessionMiddleware


class CustomSessionExpireMiddleware(SessionMiddleware):
    def process_response(self, request, response):
        # Set the session expiration based on SESSION_EXPIRE_SECONDS
        if hasattr(request, "session") and request.session.session_key:
            session_cookie_age = getattr(
                settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
            )
            response.set_cookie(
                settings.SESSION_COOKIE_NAME,
                request.session.session_key,
                max_age=session_cookie_age,
                expires=(
                    datetime.utcnow() + timedelta(seconds=session_cookie_age)
                ).strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
                domain=settings.SESSION_COOKIE_DOMAIN,
                path=settings.SESSION_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                samesite=settings.SESSION_COOKIE_SAMESITE,
            )
        return response


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            return render(request, "admin_dash_menu/error/500.html")

        return response

    def process_exception(self, request, exception):
        return render(request, "admin_dash_menu/error/404.html")


class CrossOriginOpenerPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cross-Origin-Opener-Policy"] = "same-origin"
        return response


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and active
        user = get_user(request)
        if user.is_authenticated and not user.is_active:
            return redirect("admin_login")

        return response


class DisableBackButtonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"

        else:
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        return response

    def process_request(self, request):
        if not request.user.is_authenticated and request.method == "GET":
            request.session["last_request"] = request.path

    def process_response(self, request, response):
        if request.path == "/" and "last_request" in request.session:
            del request.session["last_request"]
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return None
        if "last_request" in request.session:
            if request.path != "/" and request.path != request.session["last_request"]:
                del request.session["last_request"]
                return redirect("admin_login")
        return None
