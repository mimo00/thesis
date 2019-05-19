import datetime
from functools import partial

import pytest

from apps.decisions.factories import ScheduleDecisionFactory, DateRangeDecisionFactory
from apps.decisions.serializers import SchedulesDecisionSerializer


@pytest.mark.django_db
class TestSchedulesDecisionSerializer:
    def test_schedule_date_ranges_are_sorted(self):
        schedule_decision = ScheduleDecisionFactory()
        create_date_range = partial(DateRangeDecisionFactory, schedule_decision=schedule_decision)
        create_date_range(start_time=datetime.time(7, 30), end_time=datetime.time(10, 0))
        create_date_range(start_time=datetime.time(19, 0), end_time=datetime.time(22, 0))
        result = SchedulesDecisionSerializer(schedule_decision).data
        assert result == {
            'coverage': '50.00',
            'schedule_decision_date_ranges': [
                {'start_time': '07:30:00', 'end_time': '10:00:00'},
                {'start_time': '19:00:00', 'end_time': '22:00:00'},
            ]
        }
