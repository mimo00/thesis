import datetime
import json
import os
import shutil
from contextlib import contextmanager

from marshmallow import EXCLUDE

from aggregator.settings import TMP_DATA_DIR, DUMP_TRIPS_NAME, DISAGGREGATION_NAME, AGGREGATION_NAME
from apps.aggregator_integration.aggregator_commands import aggregate, generate_energy_market, disaggregation
from apps.aggregator_integration.generator import get_trips_data
from apps.aggregator_integration.loader import AggregatorGroupDecisionSchema, OfferSchema
from apps.decisions.models import AggregatorDecision, AggregatorGroupDecision
from apps.schedules.models import Schedule

COVERAGE = 50
MINIMUM_ENERGY_OFFER = 1000
ALL_TOGETHER = 'all_together'
BY_DESTINATIONS = 'by_destcination'



@contextmanager
def tmp_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        shutil.rmtree(path)
        os.mkdir(path)
    yield path
    pass


class AggregationService:
    def __init__(self, date: datetime.date, method=None, minimum_energy_offer=None, coverage=None):
        self.date = date
        self.method = method if method else ALL_TOGETHER
        self.minimum_energy_offer = minimum_energy_offer if minimum_energy_offer else MINIMUM_ENERGY_OFFER
        self.coverage = coverage if coverage else COVERAGE

    def generate_decision(self) -> AggregatorDecision:
        aggregate_decision = AggregatorDecision.objects.filter(decision_date=self.date)
        if aggregate_decision.exists():
            aggregate_decision.delete()
        aggregate_decision = AggregatorDecision.objects.create(decision_date=self.date,
                                                               receive_date=datetime.datetime.now(),
                                                               mode=self.get_mode())
        group_of_schedules = self.get_group_of_schedules()
        for schedules in group_of_schedules:
            self.generate_schedule(schedules, aggregate_decision)
        return aggregate_decision

    def get_mode(self):
        a = {
            ALL_TOGETHER: AggregatorDecision.GLOBAL,
            BY_DESTINATIONS: AggregatorDecision.GLOBAL,
        }
        return a[self.method]

    def get_group_of_schedules(self):
        return [Schedule.objects.filter(date__date=self.date)]

    def generate_schedule(self, schedules, aggregate_decision):
        path = self.get_path()
        with tmp_dir(path) as path:
            self.dump_schedules(path, schedules)
            aggregate(path, self.minimum_energy_offer)
            generate_energy_market(path, self.coverage)
            disaggregation(path)
            self.load_aggregated_decisions(aggregate_decision)
            self.load_offer_result(path)

    def dump_schedules(self, path, schedules):
        data = get_trips_data(schedules)
        with open(os.path.join(path, DUMP_TRIPS_NAME), "w+") as outfile:
            json.dump(data, outfile)

    def load_aggregated_decisions(self, aggregate_decision):
        path = self.get_path()
        with open(os.path.join(path, os.path.join(path, DISAGGREGATION_NAME + ".json")), "r") as file:
            data = json.load(file)
            for decision_data in data["disaggregationResultEntries"]:
                self.load_aggregated_decision(aggregate_decision, decision_data)

    def load_aggregated_decision(self, aggregate_decision, decision_data):
        group_decision, schedule_decisions = AggregatorGroupDecisionSchema(unknown=EXCLUDE).load(decision_data)
        group_decision.decision = aggregate_decision
        group_decision.group_id = decision_data["groupId"]
        group_decision.save()
        for schedule_decision, date_range_decisions in schedule_decisions:
            schedule_decision.group_decision = group_decision
            schedule_decision.save()
            for date_range_decision in date_range_decisions:
                date_range_decision.schedule_decision = schedule_decision
                date_range_decision.save()
        return group_decision

    def get_path(self):
            name_of_dir = f"{self.method}_{self.date.strftime('%Y_%m_%d')}"
            return os.path.join(TMP_DATA_DIR, name_of_dir)

    def load_offer_result(self, path):
        with open(os.path.join(path, AGGREGATION_NAME + ".json"), "r") as file:
            data = json.load(file)
            for offer_data in data["aggregatedGroups"]["aggregatedGroupsData"]:
                aggregator_group = AggregatorGroupDecision.objects.get(decision__decision_date=self.date, group_id=offer_data["groupId"])
                OfferSchema(unknown=EXCLUDE).load({**offer_data, "group_decision": aggregator_group.id})
