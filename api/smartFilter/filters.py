from django.db.models import Model
from typing import List
from django.shortcuts import get_object_or_404, get_list_or_404
from fuzzywuzzy import fuzz

from api.tariffs.models import Tariff
from api.address.models import City


class Filter:
    @staticmethod
    def tariffs(query_params: dict):
        tariffs = Tariff.objects.all().order_by("-id")
        fields = Filter._get_fields(Tariff, query_params)

        return Filter._search_tariff(fields, tariffs, query_params)

    @staticmethod
    def _search_tariff(fields, records, query_params):
        answer = []

        if not fields:
            return records[::-1]

        if "region" in fields:
            records = Filter._search_city(
                records,
                region=query_params.get("region"),
                city=query_params.get("city")
            )

            fields.remove("region")

        if "city" in fields:
            fields.remove("city")

        for record in records:
            coincidence = 0

            for field in fields:
                in_model = getattr(record, field)
                in_params = query_params.get(field).lower()

                if in_model is None or in_params is None:
                    continue

                if type(in_model) is bool:
                    in_params = True if in_params == "true" else False if in_params == "false" else in_params

                    if in_model != in_params:
                        break
                    else:
                        continue

                in_model = in_model.lower()

                coincidence_ = fuzz.ratio(
                    in_model,
                    in_params
                )

                if coincidence_ < 50:
                    break

                coincidence = coincidence_
            else:
                answer.append((record, coincidence))

        answer.sort(key=lambda x: x[1])

        return list({
            ans[0]
            for ans in answer
        })

    @staticmethod
    def _search_city(records: List[Model], region: str, city: str) -> list:
        answer = []

        if city:
            city = get_object_or_404(
                City,
                region=region,
                city=city
            )
            return records.filter(
                city=city
            )

        cities = get_list_or_404(
            City,
            region=region
        )
        return records.filter(
            city__in=cities
        )

    @staticmethod
    def _get_fields(model: Model, query_params: dict):
        fields = [
            field.name
            for field in model._meta.get_fields()
            if field.name in query_params and query_params.get(field.name, None)
        ]

        if "region" in query_params and query_params.get("region", None):
            fields.append("region")

        return fields
