from django.http import HttpResponse


class HaveRefreshTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)

        if request.path == "/api/auth/token/refresh/" and response.status_code == 401:
            return HttpResponse({ "detail": "Refresh token invalid" }, status=400)

        return response
