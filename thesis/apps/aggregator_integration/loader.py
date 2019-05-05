import datetime

import marshmallow
from marshmallow import fields, post_load, ValidationError

from apps.bids_decisions.models import AggregatorDecision, ChargingLocalizationDecision
from apps.fetching_bids.models import ChargingLocalization


class ChargingLocalizationDecisionSchema(marshmallow.Schema):
    coverage = fields.Float(required=True)
    chargeHours = fields.List(fields.Integer(), required=True, validate=lambda x: len(x) == 24)
    data = fields.Dict()

    @post_load
    def create(self, data) -> ChargingLocalizationDecision:
        charging_localization = self.get_charging_localization(data["data"])
        start_time, end_time = self.get_datetimes(data["chargeHours"], charging_localization.arrival_time)
        return ChargingLocalizationDecision(coverage=data["coverage"], start_time=start_time, end_time=end_time,
                                            charging_localization=charging_localization)

    def get_charging_localization(self, data):
        arrival_hour, departure_hour = self.get_hours(data["plugInSchedule"]["schedule"])
        return ChargingLocalization.objects.get(
            bid__electric_vehicle=data["id"], arrival_time__hour__lte=arrival_hour, departure_time__hour__gte=departure_hour)

    def get_hours(self, charge_hours):
        ACTIVE_NUM = 1
        if ACTIVE_NUM in charge_hours:
            first_index = charge_hours.index(ACTIVE_NUM)
            charge_hours.reverse()
            last_index = len(charge_hours) - 1 - charge_hours.index(ACTIVE_NUM)
            return first_index, last_index
        else:
            raise ValidationError("Nor valid time schedule")

    def get_datetimes(self, charge_hours, date):
        ACTIVE_NUM = 1
        if ACTIVE_NUM in charge_hours:
            first_index = charge_hours.index(ACTIVE_NUM)
            charge_hours.reverse()
            last_index = len(charge_hours) - 1 - charge_hours.index(ACTIVE_NUM)
            start_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=first_index, tzinfo=date.tzinfo)
            end_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=last_index+1, tzinfo=date.tzinfo)
            return start_time, end_time
        else:
            return None, None


class AggregatorDecisionSchema(marshmallow.Schema):
    totalEnergyCoverage = fields.Float(required=True)
    totalHourCoverage = fields.Float(required=True)
    totalEnergyLoss = fields.Float(required=True)
    disaggregatedTripsData = fields.List(fields.Nested(ChargingLocalizationDecisionSchema()))

    @post_load
    def create(self, data):
        decision = AggregatorDecision(energy_loss=data["totalEnergyLoss"], energy_coverage=data["totalEnergyCoverage"],
                                      hour_coverage=data["totalHourCoverage"])
        return decision, data['disaggregatedTripsData']
