from datetime import datetime, timedelta
from typing import List

import marshmallow
import attr

from marshmallow import fields

# serialization Obj -> JSON
from apps.schedules.models import Schedule
from aggregator.settings import DEADLINE_HOUR_TO_SEND_SCHEDULE


class BatteryProfileSchema(marshmallow.Schema):
    capacity = fields.Float(required=True)
    hourPercentageCharge = fields.Float(required=True)


class BatterySchema(marshmallow.Schema):
    inputEnergyLevel = fields.Float(required=True)
    outputEnergyLevel = fields.Float(required=True)
    batteryProfile = fields.Nested(BatteryProfileSchema)


class ChargingLocalizationSchema(marshmallow.Schema):
    id = fields.Integer(required=True)
    battery = fields.Nested(BatterySchema, required=True)
    plugInSchedule = fields.List(fields.Integer(), required=True)


class TripDataSchema(marshmallow.Schema):
    tripsData = fields.Nested(ChargingLocalizationSchema, many=True)


def get_beginning_of_day(date):
    return datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0, tzinfo=date.tzinfo)


@attr.s
class BatteryProfile:
    capacity = attr.ib()
    hourPercentageCharge = attr.ib()


@attr.s
class Battery:
    inputEnergyLevel = attr.ib()
    outputEnergyLevel = attr.ib()
    batteryProfile: BatteryProfile = attr.ib()


@attr.s
class TripStop:
    id: int = attr.ib()
    battery: Battery = attr.ib()
    start_date: datetime = attr.ib()
    end_date: datetime = attr.ib()

    @property
    def plugInSchedule(self) -> List[int]:
        schedule = []
        date = get_beginning_of_day(self.start_date)
        for i in range(24):
            schedule.append(1) if self.start_date < date < self.end_date else schedule.append(0)
            date += timedelta(hours=1)
        return schedule


class AggregatorInputGenerator:
    def __init__(self, date: datetime):
        self.date = date

    def generate(self):
        schedules = self.get_schedules()
        output_schedules = []
        for schedule in schedules:
            output_schedules = output_schedules + self.generate_trip_data(schedule)
        trips_data = {"tripsData": output_schedules}
        schema = TripDataSchema()
        return schema.dump(trips_data)

    def get_schedules(self):
        start_date, end_date = self._get_date_range(self.date)
        schedules = (Schedule.objects.filter(date__range=(start_date, end_date))
                              .select_related('electric_vehicle').prefetch_related('point_schedules'))
        return schedules

    @staticmethod
    def _get_date_range(date):
        start_date = datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0)
        end_date = datetime(year=date.year, month=date.month, day=date.day, hour=DEADLINE_HOUR_TO_SEND_SCHEDULE,
                            minute=0, second=0)
        return start_date, end_date

    def generate_trip_data(self, schedule):
        trip_data = []
        battery_profile = BatteryProfile(capacity=schedule.electric_vehicle.max_battery_capacity,
                                         hourPercentageCharge=schedule.electric_vehicle.max_charging_power)
        for index, point_schedule in enumerate(schedule.point_schedules.all()):
            battery = Battery(inputEnergyLevel=point_schedule.charge_percent, batteryProfile=battery_profile,
                              outputEnergyLevel=point_schedule.expected_charge_percent)
            trip_stop = TripStop(id=point_schedule.schedule.electric_vehicle.id, battery=battery, start_date=point_schedule.arrival_time,
                                 end_date=point_schedule.departure_time)
            trip_data.append(trip_stop)
        return trip_data
