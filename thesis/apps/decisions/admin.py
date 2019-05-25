from django.contrib import admin
from apps.decisions import models
from django.contrib.auth.models import Group

from apps.decisions.models import Offer, EnergyHourOffer


class AggregatorDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'decision_date', 'receive_date')


class AggregatorGroupDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'energy_coverage', 'hour_coverage', 'energy_loss')


class ScheduleDecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_decision', 'schedule', 'coverage')


admin.site.register(models.AggregatorDecision, AggregatorDecisionAdmin)
admin.site.register(models.AggregatorGroupDecision, AggregatorGroupDecisionAdmin)
admin.site.register(models.ScheduleDecision, ScheduleDecisionAdmin)
admin.site.register(Offer)
admin.site.register(EnergyHourOffer)
admin.site.unregister(Group)
