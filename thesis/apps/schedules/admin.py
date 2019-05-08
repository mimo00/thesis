from django.contrib import admin
from apps.schedules import models


class ElectricVehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'max_battery_capacity', 'min_battery_capacity', 'max_charging_power', 'user')


class PointScheduleInline(admin.TabularInline):
    model = models.PointSchedule
    extra = 0


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'mode', 'electric_vehicle')
    inlines = [
        PointScheduleInline
    ]


admin.site.register(models.ElectricVehicle, ElectricVehicleAdmin)
admin.site.register(models.Node)
admin.site.register(models.ChargingPoint)
admin.site.register(models.Schedule, ScheduleAdmin)
admin.site.register(models.PointSchedule)
