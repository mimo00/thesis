from datetime import datetime

import pytest

from apps.aggregator_integration.generator import TripStopSchema, get_trip_data, get_trips_data
from apps.schedules.factories import PointScheduleFactory, ElectricVehicleFactory, ScheduleFactory


@pytest.mark.django_db
def test_getting_trip_data():
    ev = ElectricVehicleFactory(max_battery_capacity=100, min_battery_capacity=20, max_charging_power=10)
    schedule = ScheduleFactory(charge_percent=20.00, trip_percent=70.00, electric_vehicle=ev)
    charging_date = datetime(year=2019, month=7, day=24, hour=6, minute=30)
    PointScheduleFactory(schedule=schedule, arrival_time=charging_date.replace(hour=6, minute=30),
                         departure_time=charging_date.replace(hour=12, minute=10))
    trip_data = get_trip_data(schedule)
    result = TripStopSchema().dump(trip_data)
    assert result == {
        'plugInSchedule': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'battery': {
            'batteryProfile': {
                'hourPercentageCharge': 10.0,
                'capacity': 100.0
            },
            'inputEnergyLevel': 20.0,
            'outputEnergyLevel': 90.0
        },
        "id": ev.id
    }


@pytest.mark.django_db
def test_getting_trips_data():
    charging_date = datetime(year=2019, month=7, day=24)
    ev1 = ElectricVehicleFactory(max_battery_capacity=100, min_battery_capacity=20, max_charging_power=10)
    ev2 = ElectricVehicleFactory(max_battery_capacity=100, min_battery_capacity=20, max_charging_power=10)
    schedule1 = ScheduleFactory(charge_percent=20.00, trip_percent=70.00, electric_vehicle=ev1)
    schedule2 = ScheduleFactory(charge_percent=20.00, trip_percent=70.00, electric_vehicle=ev2)
    PointScheduleFactory(arrival_time=charging_date.replace(hour=6, minute=30),
                         departure_time=charging_date.replace(hour=12, minute=10), schedule=schedule1)
    PointScheduleFactory(arrival_time=charging_date.replace(hour=6, minute=30),
                         departure_time=charging_date.replace(hour=12, minute=10), schedule=schedule2)
    result = get_trips_data([schedule1, schedule2])
    assert result == {
        "tripsData": [
            {
                'plugInSchedule': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'battery': {
                    'batteryProfile': {
                        'hourPercentageCharge': 10.0,
                        'capacity': 100.0
                    },
                    'inputEnergyLevel': 20.0,
                    'outputEnergyLevel': 90.0
                },
                "id": ev1.id
            },
            {
                'plugInSchedule': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'battery': {
                    'batteryProfile': {
                        'hourPercentageCharge': 10.0,
                        'capacity': 100.0
                    },
                    'inputEnergyLevel': 20.0,
                    'outputEnergyLevel': 90.0
                },
                "id": ev2.id
            }
        ]
    }

