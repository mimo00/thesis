from django.db import models

from apps.fetching_bids.models import Bid, ChargingLocalization


class AggregatorDecision(models.Model):
    decision_date = models.DateField(unique=True)
    receive_date = models.DateTimeField()
    energy_coverage = models.DecimalField(max_digits=5, decimal_places=2)
    hour_coverage = models.DecimalField(max_digits=5, decimal_places=2)
    energy_loss = models.DecimalField(max_digits=5, decimal_places=2)


class ChargingLocalizationDecision(models.Model):
    decision = models.ForeignKey(AggregatorDecision, on_delete=models.CASCADE,
                                 related_name="charging_localization_decisions")
    charging_localization = models.OneToOneField(ChargingLocalization, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    coverage = models.DecimalField(max_digits=5, decimal_places=2)
