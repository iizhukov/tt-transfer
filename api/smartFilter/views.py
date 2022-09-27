from rest_framework.views import APIView
from rest_framework.request import Request
from typing import List

from api.tariffs.models import Tariff


class TariffFilterView(APIView):
    def get(self, request: Request):
        name = request.query_params.get("name")
        city = request.query_params.get("city")

        tariffs: List[Tariff] = Tariff.objects.all()

        answer = []

        if name:
            for tariff in tariffs:
                tariff.title
