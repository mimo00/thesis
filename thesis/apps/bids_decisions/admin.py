from django.contrib import admin
from apps.bids_decisions import models


class ChargingLocalizationDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'decision', 'charging_localization', 'start_time', 'end_time', 'coverage')


class AggregatorDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'decision_date', 'receive_date', 'energy_coverage', 'hour_coverage', 'energy_loss')


admin.site.register(models.ChargingLocalizationDecision, ChargingLocalizationDecisionAdmin)
admin.site.register(models.AggregatorDecision, AggregatorDecisionAdmin)
