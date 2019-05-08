from datetime import datetime

import marshmallow
from marshmallow import fields, post_load, ValidationError, EXCLUDE
from pytz import UTC

from apps.aggregator_integration.time_utils import get_index_range, get_date_range
from apps.decisions.models import AggregatorDecision, PointScheduleDecision
from apps.schedules.models import PointSchedule


class ChargingLocalizationDecisionSchema(marshmallow.Schema):
    coverage = fields.Float(required=True)
    chargeHours = fields.List(fields.Integer(), required=True, validate=lambda x: len(x) == 24)
    data = fields.Dict()

    @post_load
    def create(self, data) -> PointScheduleDecision:
        point_schedule = self.get_point_schedule(data["data"])
        date_range = get_date_range(data["chargeHours"], point_schedule.arrival_time)
        return PointScheduleDecision(coverage=data["coverage"], start_time=date_range.start,
                                             end_time=date_range.end, point_schedule=point_schedule)

    def get_point_schedule(self, data):
        arrival_hour, departure_hour = self.get_hours(data["plugInSchedule"]["schedule"])
        now = datetime.now(tz=UTC)
        return PointSchedule.objects.get(
            schedule__electric_vehicle=data["id"], arrival_time__hour__lte=arrival_hour,
            departure_time__hour__gte=departure_hour, schedule__date__date=now)

    def get_hours(self, charge_hours):
        index_range = get_index_range(charge_hours)
        if not index_range.is_empty:
            return index_range.start, index_range.end
        else:
            raise ValidationError("Nor valid time schedule")


class AggregatorDecisionSchema(marshmallow.Schema):
    totalEnergyCoverage = fields.Float(required=True)
    totalHourCoverage = fields.Float(required=True)
    totalEnergyLoss = fields.Float(required=True)
    totalNumberOfSchemes = fields.Integer(required=True)
    disaggregatedTripsData = fields.List(fields.Nested(ChargingLocalizationDecisionSchema(unknown=EXCLUDE)))

    @post_load
    def create(self, data):
        decision = AggregatorDecision(energy_loss=data["totalEnergyLoss"], energy_coverage=data["totalEnergyCoverage"],
                                      hour_coverage=data["totalHourCoverage"])
        return decision, data['disaggregatedTripsData']
