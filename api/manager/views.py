from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ManagerView(APIView):
    def get(self, request):
        return Response(
            {
                "detail": "What`s up, bro!"
            },
            status=status.HTTP_200_OK
        )