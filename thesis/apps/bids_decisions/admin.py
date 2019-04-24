from django.contrib import admin
from apps.bids_decisions import models


class ChargingLocalizationDecisionInline(admin.TabularInline):
    model = models.ChargingLocalizationDecision
    extra = 0


class BidDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'bid')

    inlines = [
        ChargingLocalizationDecisionInline
    ]


class AggregatorDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'decision_date', 'receive_date', 'energy_coverage', 'hour_coverage', 'energy_loss')


admin.site.register(models.BidDecision, BidDecisionAdmin)
admin.site.register(models.AggregatorDecision, AggregatorDecisionAdmin)
