from datetime import datetime, date

import factory

from apps.decisions.models import AggregatorDecision, ScheduleDecision, AggregatorGroupDecision, DateRangeDecision
from apps.schedules.factories import ScheduleFactory


class AggregatorDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = AggregatorDecision

    decision_date = date(2020, 5, 3)
    receive_date = datetime(2020, 5, 3, 23, 30)
    mode = "glob"


class AggregatorGroupDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = AggregatorGroupDecision
    is_success = True
    decision = factory.SubFactory(AggregatorDecisionFactory)
    energy_coverage = 75.00
    hour_coverage = 60.00
    energy_loss = 2.5
    group_id = 1


class ScheduleDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = ScheduleDecision

    group_decision = factory.SubFactory(AggregatorGroupDecisionFactory)
    schedule = factory.SubFactory(ScheduleFactory)
    coverage = 50.00


class DateRangeDecisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = DateRangeDecision

    start_time = datetime(year=2019, month=7, day=24, hour=7, minute=0)
    end_time = datetime(year=2019, month=7, day=24, hour=10, minute=0)
