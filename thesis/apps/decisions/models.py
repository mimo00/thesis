from django.db import models

from apps.schedules.models import Schedule, PointSchedule


class AggregatorDecision(models.Model):
    decision_date = models.DateField(unique=True)
    receive_date = models.DateTimeField()
    energy_coverage = models.DecimalField(max_digits=5, decimal_places=2)
    hour_coverage = models.DecimalField(max_digits=5, decimal_places=2)
    energy_loss = models.DecimalField(max_digits=5, decimal_places=2)


class PointScheduleDecision(models.Model):
    decision = models.ForeignKey(AggregatorDecision, on_delete=models.CASCADE,
                                 related_name="point_schedule_decisions")
    point_schedule = models.OneToOneField(PointSchedule, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    coverage = models.DecimalField(max_digits=5, decimal_places=2)
