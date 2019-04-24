from django.db import models

from apps.fetching_bids.models import Bid, ChargingLocalization


class AggregatorDecision(models.Model):
    decision_date = models.DateField(unique=True)
    receive_date = models.DateTimeField()
    decision = models.BooleanField()


class BidDecision(models.Model):
    decision = models.ForeignKey(AggregatorDecision, on_delete=models.CASCADE)
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE)


class ChargingLocalizationDecision(models.Model):
    bid_decision = models.ForeignKey(BidDecision, on_delete=models.CASCADE,
                                     related_name="charging_localization_decisions")
    charging_localization = models.OneToOneField(ChargingLocalization, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    coverage = models.DecimalField(max_digits=5, decimal_places=2)