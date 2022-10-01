from django.db.models import Model
from typing import List
from django.shortcuts import get_object_or_404, get_list_or_404
from fuzzywuzzy import fuzz

from api.tariffs.models import Tariff
from api.address.models import City


class Filter:
    @staticmethod
    def tariffs(query_params: dict):
        tariffs = Tariff.objects.all()
        fields = Filter._get_fields(Tariff, query_params)

        return Filter._search(fields, tariffs, query_params)

    @staticmethod
    def _search(fields, records, query_params):
        answer = []

        print(fields)

        if "region" in fields:
            records = Filter._search_city(
                records,
                region=query_params.get("region"),
                city=query_params.get("city")
            )

            fields.remove("region")

        if "city" in fields:
            fields.remove("city")

        if not fields:
            return records[::-1]

        for field in fields:
            for record in records:
                in_model = getattr(record, field)
                in_params = query_params.get(field, "")

                print(in_model, in_params)

                if type(in_model) == bool and in_params.lower() in ("true", "false"):
                    in_params = True if in_params.lower() in "true" else False

                    if in_model == in_params:
                        answer.append((record, 100))
                    continue

                coincidence = fuzz.ratio(
                    in_model,
                    in_params
                )

                if in_params == in_model:
                    answer.append((record, 100))

                elif coincidence >= 50 or in_params in in_model:
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
