from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from .models import City


class CityIndex(Document.DocType):
    pk = fields.Integer()
    # country = fields.()
    region = fields.Text()
    city = fields.Text()

    class Meta:
        model = City
        index = 'city'
