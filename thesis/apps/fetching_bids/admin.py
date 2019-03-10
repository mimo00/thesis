from django.contrib import admin
from apps.fetching_bids import models

admin.site.register(models.ElectricVehicle)
admin.site.register(models.Node)
admin.site.register(models.Generator)
