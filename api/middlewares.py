from django.http import HttpResponse
from rest_framework import status


class HaveRefreshTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)

        if request.path == "/api/auth/token/refresh/" and response.status_code == 401:
            return HttpResponse(
                {"detail": "Refresh token invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return response


class HaveTokenToMediaMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request):
        print(request.user, request.user.is_authenticated)
        if "/media/news/" in request.path and request.user.is_authenticated:
            return HttpResponse(
                {"detail": "Not enough rights"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = self._get_response(request)

        return response
