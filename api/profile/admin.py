from django.contrib import admin

from .models import Company
from api.authentication.models import UserDocument


admin.site.register(Company)
admin.site.register(UserDocument)
