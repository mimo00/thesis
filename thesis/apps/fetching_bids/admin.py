from django.contrib import admin
from apps.fetching_bids import models


class ElectricVehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'max_battery_capacity', 'min_battery_capacity', 'max_charging_power', 'user')


class ChargingLocalizationInline(admin.TabularInline):
    model = models.ChargingLocalization
    extra = 0


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'mode', 'electric_vehicle')
    inlines = [
        ChargingLocalizationInline
    ]


admin.site.register(models.ElectricVehicle, ElectricVehicleAdmin)
admin.site.register(models.Node)
admin.site.register(models.Localization)
admin.site.register(models.Bid, BidAdmin)
admin.site.register(models.ChargingLocalization)
