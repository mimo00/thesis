from datetime import datetime, date

import factory

from apps.decisions.models import AggregatorDecision, PointScheduleDecision
from apps.schedules.factories import PointScheduleFactory


class AggregatorDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = AggregatorDecision

    decision_date = date(2020, 5, 3)
    receive_date = datetime(2020, 5, 3, 23, 30)
    energy_coverage = 75.00
    hour_coverage = 60.00
    energy_loss = 2.5


class ChargingLocalizationDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = PointScheduleDecision

    decision = factory.SubFactory(AggregatorDecisionFactory)
    point_schedule = factory.SubFactory(PointScheduleFactory)
    start_time = datetime(year=2019, month=7, day=24, hour=7, minute=0)
    end_time = datetime(year=2019, month=7, day=24, hour=10, minute=0)
    coverage = 50.00