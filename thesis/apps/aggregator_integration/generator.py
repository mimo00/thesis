from datetime import datetime, timedelta
from typing import List

import marshmallow
import attr

from marshmallow import fields

# serialization Obj -> JSON
from apps.fetching_bids.models import Bid
from evs_bids.settings import DEADLINE_HOUR_TO_SEND_BID


class BatteryProfileSchema(marshmallow.Schema):
    capacity = fields.Float(required=True)
    hourPercentageCharge = fields.Float(required=True)


class BatterySchema(marshmallow.Schema):
    inputEnergyLevel = fields.Float(required=True)
    outputEnergyLevel = fields.Float(required=True)
    batteryProfile = fields.Nested(BatteryProfileSchema)


class ChargingLocalizationSchema(marshmallow.Schema):
    localization = fields.Integer(required=True)
    battery = fields.Nested(BatterySchema, required=True)
    plugInSchedule = fields.List(fields.Integer(), required=True)


class TripDataSchema(marshmallow.Schema):
    tripsData = fields.List(fields.Nested(ChargingLocalizationSchema, many=True))


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
    localization = attr.ib()
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
        bids = self.get_bids()
        output_bids = []
        for bid in bids:
            output_bids.append(self.generate_trip_data(bid))
        trips_data = {"tripsData": output_bids}
        schema = TripDataSchema()
        return schema.dump(trips_data)

    def get_bids(self):
        start_date, end_date = self._get_date_range(self.date)
        bids = (Bid.objects.filter(date__range=(start_date, end_date))
                .select_related('electric_vehicle').prefetch_related('charging_localizations'))
        return bids

    @staticmethod
    def _get_date_range(date):
        start_date = datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0)
        end_date = datetime(year=date.year, month=date.month, day=date.day, hour=DEADLINE_HOUR_TO_SEND_BID,
                            minute=0, second=0)
        return start_date, end_date

    def generate_trip_data(self, bid):
        trip_data = []
        battery_profile = BatteryProfile(capacity=bid.electric_vehicle.max_battery_capacity,
                                         hourPercentageCharge=bid.electric_vehicle.max_charging_power)
        for index, charging_localization in enumerate(bid.charging_localizations.all()):
            battery = Battery(inputEnergyLevel=charging_localization.charge_percent, batteryProfile=battery_profile,
                              outputEnergyLevel=charging_localization.expected_charge_percent)
            trip_stop = TripStop(localization=index, battery=battery, start_date=charging_localization.arrival_time,
                                 end_date=charging_localization.departure_time)
            trip_data.append(trip_stop)
        return trip_data
