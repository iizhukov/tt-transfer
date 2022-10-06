from django.contrib import admin

from . import models
from api.authentication.models import UserDocument

admin.site.register(UserDocument)

admin.site.register(models.Company)
admin.site.register(models.BankModel)
admin.site.register(models.EmployeeModel)
admin.site.register(models.Client)
admin.site.register(models.Manager)
admin.site.register(models.Admin)
admin.site.register(models.Driver)
#
