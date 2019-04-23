from datetime import datetime, date

import factory

from apps.bids_decisions.models import AggregatorDecision, BidDecision, ChargingLocalizationDecision
from apps.fetching_bids.factories import BidFactory, ChargingLocalizationFactory


class AggregatorDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = AggregatorDecision

    decision_date = date(2020, 5, 3)
    receive_date = datetime(2020, 5, 3, 23, 30)
    decision = True


class BidDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = BidDecision

    decision = factory.SubFactory(AggregatorDecisionFactory)
    bid = factory.SubFactory(BidFactory)


class ChargingLocalizationDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = ChargingLocalizationDecision

    bid_decision = factory.SubFactory(BidDecisionFactory)
    charging_localization = factory.SubFactory(ChargingLocalizationFactory)
    start_time = datetime(year=2019, month=7, day=24, hour=7, minute=0)
    end_time = datetime(year=2019, month=7, day=24, hour=10, minute=0)
    coverage = 50.00
