from django.contrib.postgres.forms import JSONField
from django.db import models

from apps.schedules.models import Schedule


class AggregatorDecision(models.Model):
    GLOBAL = 'global'
    BY_NODE = 'by_localization'
    TYPES = (
        (GLOBAL, 'global'),
        (BY_NODE, 'by_loc'),
    )
    mode = models.CharField(max_length=6, choices=TYPES)
    decision_date = models.DateField(unique=True)
    receive_date = models.DateTimeField()


class AggregatorGroupDecision(models.Model):
    decision = models.ForeignKey(AggregatorDecision, on_delete=models.CASCADE, related_name="aggregator_group_decisions")
    group_params = JSONField()
    is_success = models.BooleanField()
    energy_coverage = models.DecimalField(max_digits=5, decimal_places=2)
    hour_coverage = models.DecimalField(max_digits=5, decimal_places=2)
    energy_loss = models.DecimalField(max_digits=5, decimal_places=2)
    group_id = models.IntegerField()


class Offer(models.Model):
    group_decision = models.OneToOneField(AggregatorGroupDecision, on_delete=models.CASCADE, related_name="offer")
    number_of_schemas = models.IntegerField()
    total_energy = models.IntegerField()


class EnergyHourOffer(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="hour_offers")
    hour_index = models.IntegerField()
    energy = models.IntegerField()


class ScheduleDecision(models.Model):
    group_decision = models.ForeignKey(AggregatorGroupDecision, on_delete=models.CASCADE,
                                       related_name="schedule_decisions")
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE)
    coverage = models.DecimalField(max_digits=5, decimal_places=2)


class DateRangeDecision(models.Model):
    schedule_decision = models.ForeignKey(ScheduleDecision, on_delete=models.CASCADE,
                                          related_name="schedule_decision_date_ranges")
    start_time = models.TimeField()
    end_time = models.TimeField()
