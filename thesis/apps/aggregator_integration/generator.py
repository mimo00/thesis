from datetime import datetime, timedelta
from typing import List

import marshmallow
import attr

from marshmallow import fields

# serialization Obj -> JSON
from apps.aggregator_integration.time_utils import get_schedule
from apps.schedules.models import Schedule, Node, PointSchedule
from aggregator.settings import DEADLINE_HOUR_TO_SEND_SCHEDULE


class BatteryProfileSchema(marshmallow.Schema):
    capacity = fields.Float(required=True)
    hourPercentageCharge = fields.Float(required=True)


class BatterySchema(marshmallow.Schema):
    inputEnergyLevel = fields.Float(required=True)
    outputEnergyLevel = fields.Float(required=True)
    batteryProfile = fields.Nested(BatteryProfileSchema)


class TripStopSchema(marshmallow.Schema):
    id = fields.Integer(required=True)
    battery = fields.Nested(BatterySchema, required=True)
    plugInSchedule = fields.List(fields.Integer(), required=True)


class TripDataSchema(marshmallow.Schema):
    tripsData = fields.Nested(TripStopSchema, many=True)


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
        return get_schedule(self.start_date.hour, self.end_date.hour)


def get_trip_data(start_date: datetime, end_date: datetime, node: Node):
    trips_stops = get_trip_stops(start_date, end_date, node)
    return TripDataSchema().dump({"tripsData": trips_stops})


def get_trip_stops(start_date: datetime, end_date: datetime, node: Node) -> List[TripStop]:
    trip_stops = []
    point_schedules = (PointSchedule.objects
                       .filter(point__node=node, schedule__date__range=(start_date, end_date))
                       .select_related('schedule__electric_vehicle'))
    for point_schedule in point_schedules:
        trip_stops.append(get_trip_stop(point_schedule))
    return trip_stops


def get_trip_stop(point_schedule: PointSchedule) -> TripStop:
    electric_vehicle = point_schedule.schedule.electric_vehicle
    battery_profile = BatteryProfile(capacity=electric_vehicle.max_battery_capacity,
                                     hourPercentageCharge=electric_vehicle.max_charging_power)
    battery = Battery(batteryProfile=battery_profile,
                      inputEnergyLevel=point_schedule.charge_percent,
                      outputEnergyLevel=point_schedule.expected_charge_percent)
    trip_stop = TripStop(id=electric_vehicle.id,
                         battery=battery,
                         start_date=point_schedule.arrival_time,
                         end_date=point_schedule.departure_time)
    return trip_stop
