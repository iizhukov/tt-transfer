from django.http import HttpResponse

from api.authentication.models import UserDocument


class HaveRefreshTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)

        if request.path == "/api/auth/token/refresh/" and response.status_code == 401:
            return HttpResponse(
                "Refresh token invalid",
                status=400
            )

        return response


class HaveTokenToMediaMiddleware:
    def __init__(self, get_response) -> None:
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)

        print(request.user, request.user.is_authenticated)
        if "/media/documents/" in request.path:
            if not request.user.is_authenticated:
                return HttpResponse(
                    "Not enough rights",
                    status=401
                )

            docs = UserDocument.objects.filter(user=request.user).values_list("document")
            print(docs)
            for i in docs:
                if "/media/" + i[0] in request.path:
                    break
            else:
                return HttpResponse(
                    "Not enough rights",
                    status=401
                )

        if "/media/news/" in request.path and not request.user.is_authenticated:
            return HttpResponse(
                "Not enough rights",
                status=401
            )

        return response
