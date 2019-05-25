from datetime import datetime
from typing import List

import marshmallow
from marshmallow import fields, post_load, ValidationError, EXCLUDE
from pytz import UTC

from apps.aggregator_integration.time_utils import get_index_range, get_time_ranges
from apps.decisions.models import ScheduleDecision, AggregatorGroupDecision, DateRangeDecision, Offer, EnergyHourOffer
from apps.schedules.models import PointSchedule, Schedule


class ScheduleDecisionSchema(marshmallow.Schema):
    coverage = fields.Float(required=True)
    chargeHours = fields.List(fields.Integer(), required=True, validate=lambda x: len(x) == 24)
    data = fields.Dict()

    @post_load
    def create(self, data) -> (ScheduleDecision, List[DateRangeDecision]):
        schedule = self.get_point_schedule(data["data"])
        schedule_decision = ScheduleDecision(coverage=data["coverage"], schedule=schedule)
        date_ranges = self.get_date_ranges_decision(data["chargeHours"])
        return schedule_decision, date_ranges

    def get_point_schedule(self, data):
        now = datetime.now(tz=UTC)
        return Schedule.objects.get(electric_vehicle=data["id"], date__date=now)

    def get_hours(self, charge_hours):
        index_range = get_index_range(charge_hours)
        if not index_range.is_empty:
            return index_range.start, index_range.end
        else:
            raise ValidationError("Nor valid time schedule")

    def get_date_ranges_decision(self, plugin_schedule) -> List[DateRangeDecision]:
        time_ranges = get_time_ranges(plugin_schedule)
        date_ranges_decision = []
        for time_range in time_ranges:
            date_ranges_decision.append(DateRangeDecision(start_time=time_range[0], end_time=time_range[1]))
        return date_ranges_decision


class AggregatorGroupDecisionSchema(marshmallow.Schema):
    totalEnergyCoverage = fields.Float(required=True)
    totalHourCoverage = fields.Float(required=True)
    totalEnergyLoss = fields.Float(required=True)
    totalNumberOfSchemes = fields.Integer(required=True)
    disaggregatedTripsData = fields.List(fields.Nested(ScheduleDecisionSchema(unknown=EXCLUDE)))

    @post_load
    def create(self, data):
        decision = AggregatorGroupDecision(is_success=True, energy_loss=data["totalEnergyLoss"],
                                           energy_coverage=data["totalEnergyCoverage"],
                                           hour_coverage=data["totalHourCoverage"])
        return decision, data['disaggregatedTripsData']


class OfferSchema(marshmallow.Schema):
    group_decision = fields.Integer()
    energyDemands = fields.List(fields.Float())
    totalEnergyDemand = fields.Integer()
    totalNumberOfSchemes = fields.Integer()

    @post_load
    def create(self, data):
        group_decision = AggregatorGroupDecision.objects.get(id=data["group_decision"])
        offer = Offer.objects.create(
            number_of_schemas=data["totalNumberOfSchemes"], total_energy=data["totalEnergyDemand"], group_decision=group_decision)
        for index, energy_value in enumerate(data["energyDemands"]):
            EnergyHourOffer.objects.create(hour_index=index, energy=energy_value, offer=offer)
        return offer


