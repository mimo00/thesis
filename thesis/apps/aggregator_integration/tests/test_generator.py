from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from dateutil.tz import UTC
from freezegun import freeze_time

from apps.aggregator_integration.generator import AggregatorInputGenerator, TripStop
from apps.schedules.factories import ScheduleFactory, PointScheduleFactory, ElectricVehicleFactory

test_date = datetime(year=2019, month=4, day=15, hour=16, minute=30, second=34, tzinfo=UTC)
DAY = timedelta(days=1)


class TestTripStop:
    def test_generating_plug_in_schedule(self):
        start_date = datetime(year=2019, month=4, day=15, hour=6, minute=30, second=0, tzinfo=UTC)
        end_date = datetime(year=2019, month=4, day=15, hour=15, minute=30, second=0, tzinfo=UTC)
        trip_stop = TripStop(id=1, start_date=start_date, end_date=end_date, battery=Mock())
        assert trip_stop.plugInSchedule == [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]


@pytest.mark.django_db
class TestAggregatorInputGenerator:
    def test_getting_schedules(self):
        with freeze_time(test_date):
            ScheduleFactory()
        with freeze_time(test_date+DAY):
            ScheduleFactory()
        aig = AggregatorInputGenerator(date=test_date)
        schedules = aig.get_schedules()
        assert len(schedules) == 1

    def test_generate_input(self):
        ev = ElectricVehicleFactory(max_battery_capacity=100, min_battery_capacity=20, max_charging_power=10)
        with freeze_time(test_date):
            schedule = ScheduleFactory(electric_vehicle=ev)
        PointScheduleFactory(arrival_time=datetime(year=2019, month=7, day=24, hour=6, minute=30),
                                     departure_time=datetime(year=2019, month=7, day=24, hour=14, minute=30),
                                     charge_percent=20.00, expected_charge_percent=70.00, schedule=schedule)
        PointScheduleFactory(arrival_time=datetime(year=2019, month=7, day=24, hour=17, minute=30),
                                     departure_time=datetime(year=2019, month=7, day=24, hour=23, minute=59),
                                     charge_percent=10.00, expected_charge_percent=99.99, schedule=schedule)
        generator = AggregatorInputGenerator(date=test_date)
        data = generator.generate()
        assert data == {
            "tripsData": [
                {
                    'plugInSchedule': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'battery': {
                        'batteryProfile': {
                            'hourPercentageCharge': 10.0,
                            'capacity': 100.0
                        },
                        'inputEnergyLevel': 20.0,
                        'outputEnergyLevel': 70.0
                    },
                    "id": ev.id
                },
                {
                    'plugInSchedule': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                    'battery': {
                        'batteryProfile': {
                            'hourPercentageCharge': 10.0,
                            'capacity': 100.0
                        },
                        'inputEnergyLevel': 10.0,
                        'outputEnergyLevel': 99.99
                    },
                    "id": ev.id
                }
            ]
        }


