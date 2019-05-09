from django.contrib import admin
from apps.decisions import models


class PointScheduleDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'decision', 'point_schedule', 'start_time', 'end_time', 'coverage')


class AggregatorDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'decision_date', 'receive_date', 'energy_coverage', 'hour_coverage', 'energy_loss')


admin.site.register(models.PointScheduleDecision, PointScheduleDecisionAdmin)
admin.site.register(models.AggregatorDecision, AggregatorDecisionAdmin)
