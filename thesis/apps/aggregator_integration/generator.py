from datetime import datetime, timedelta
from typing import List

import marshmallow
import attr

from marshmallow import fields

# serialization Obj -> JSON
from apps.aggregator_integration.time_utils import get_schedule, get_plugin_schedule
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
class TripData:
    id: int = attr.ib()
    battery: Battery = attr.ib()
    plugInSchedule = attr.ib()


def get_trips_data(schedules: List[Schedule]):
    trips_data = []
    for schedule in schedules:
        trips_data.append(get_trip_data(schedule))
    return TripDataSchema().dump({"tripsData": trips_data})


def get_trip_data(schedule: Schedule) -> TripData:
    electric_vehicle = schedule.electric_vehicle
    battery_profile = BatteryProfile(capacity=electric_vehicle.max_battery_capacity,
                                     hourPercentageCharge=electric_vehicle.max_charging_power)
    battery = Battery(batteryProfile=battery_profile,
                      inputEnergyLevel=schedule.charge_percent,
                      outputEnergyLevel=schedule.charge_percent + schedule.trip_percent)
    trip_stop = TripData(id=electric_vehicle.id, battery=battery,
                         plugInSchedule=get_plugin_schedule(get_time_ranges(schedule.point_schedules)))
    return trip_stop


def get_time_ranges(point_schedules: List[PointSchedule]):
    time_ranges = []
    for point_schedule in point_schedules.all():
        time_ranges.append((point_schedule.arrival_time.time(), point_schedule.departure_time.time()))
    return time_ranges

