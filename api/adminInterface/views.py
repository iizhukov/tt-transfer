from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from api.permissions import IsAdminUser
from api.profile.serializers import ManagerSerializer
from api.profile.models import Manager


class AdminManagersView(APIView):
    serialiaer_class = ManagerSerializer
    permission_classes = (IsAdminUser, )

    def get(self, request):
        active_managers_serializer = self.serialiaer_class(
            Manager.objects.filter(
                user__is_active=True
            ),
            many=True
        )
        not_active_managers_serializer = self.serialiaer_class(
            Manager.objects.filter(
                user__is_active=False
            ),
            many=True
        )

        return Response(
            {
                "active": active_managers_serializer.data,
                "not_active": not_active_managers_serializer.data
            },
            status.HTTP_200_OK
        )
