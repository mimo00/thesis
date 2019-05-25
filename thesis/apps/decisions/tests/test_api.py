import datetime

import pytest
from django.urls import reverse
from freezegun import freeze_time
from pytz import UTC
from rest_framework import status

from apps.decisions.factories import ScheduleDecisionFactory, AggregatorDecisionFactory, DateRangeDecisionFactory
from apps.schedules.factories import ElectricVehicleFactory

test_date = datetime.datetime(year=2019, month=4, day=15, hour=16, minute=30, tzinfo=UTC)
DAY = datetime.timedelta(days=1)


@pytest.mark.django_db
class TestScheduleDecisionView:
    def test_getting_list_of_decisions(self, auth_api_client):
        e_v = ElectricVehicleFactory(user=auth_api_client.user)
        ScheduleDecisionFactory(group_decision__decision__decision_date=test_date - DAY, schedule__electric_vehicle=e_v)
        ScheduleDecisionFactory(group_decision__decision__decision_date=test_date, schedule__electric_vehicle=e_v)
        url = reverse("charging_schedules_decision-list")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": e_v.id})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 2

    def test_getting_filter_by_date(self, auth_api_client):
        e_v = ElectricVehicleFactory(user=auth_api_client.user)
        ScheduleDecisionFactory(group_decision__decision__decision_date=test_date - DAY, schedule__electric_vehicle=e_v)
        ScheduleDecisionFactory(group_decision__decision__decision_date=test_date, schedule__electric_vehicle=e_v)
        url = reverse("charging_schedules_decision-list")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": e_v.id, "date": test_date.date()})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1

    def test_getting_schedule_decision(self, auth_api_client):
        decision = AggregatorDecisionFactory(decision_date=test_date + DAY)
        e_v = ElectricVehicleFactory(user=auth_api_client.user)
        schedule_decision = ScheduleDecisionFactory(
            group_decision__decision=decision, schedule__electric_vehicle=e_v, coverage=30.0)
        DateRangeDecisionFactory(
            schedule_decision=schedule_decision,
            start_time=datetime.time(7, 30, tzinfo=UTC),
            end_time=datetime.time(10, 0, tzinfo=UTC)
        )
        url = reverse("charging_schedules_decision-next-day")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": e_v.id})
        assert res.status_code == status.HTTP_200_OK
        assert res.data['coverage'] == '30.00'
        assert res.data['schedule_decision_date_ranges'] == [
            {'start_time': '07:30:00', 'end_time': '10:00:00'}
        ]

    def test_getting_schedule_decision_for_not_permitted_vehicle(self, auth_api_client):
        AggregatorDecisionFactory(decision_date=test_date + DAY)
        e_v = ElectricVehicleFactory()
        url = reverse("charging_schedules_decision-next-day")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": e_v.id})
        assert res.status_code == status.HTTP_403_FORBIDDEN
        assert res.data["detail"] == f"You are trying to get schedule for electric vehicle: {e_v.id} but it is not assigned for your account"

    def test_getting_schedule_decision_while_there_is_no_decision(self, auth_api_client):
        fake_electric_vehicle = 123
        expected_checking_date = datetime.datetime(year=2019, month=4, day=16, hour=16, minute=30, tzinfo=UTC)
        url = reverse("charging_schedules_decision-next-day")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": fake_electric_vehicle})
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.data["error"] == f"There is no decision for day {expected_checking_date}"

