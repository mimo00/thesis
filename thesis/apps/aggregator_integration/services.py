import json
import os
import shutil
from contextlib import contextmanager
from datetime import datetime, time

from dateutil.tz import UTC
from marshmallow import EXCLUDE

from aggregator.settings import TMP_DATA_DIR, DEADLINE_HOUR_TO_SEND_SCHEDULE, \
    DUMP_TRIPS_NAME, DISAGGREGATION_NAME
from apps.aggregator_integration.aggregator_commands import aggregate, generate_energy_market, disaggregation
from apps.aggregator_integration.generator import get_trip_data
from apps.aggregator_integration.loader import AggregatorNodeDecisionSchema
from apps.decisions.models import AggregatorDecision
from apps.schedules.models import Node


def generate_decision():
    nodes = Node.objects.all()
    today = datetime.now()
    for node in nodes:
        generate_decision_for_node(today.date(), node)
    # a_d = AggregatorDecision.objects.filter(decision_date=today.date())
    # if a_d.exists():
    #     a_d.delete()
    # data = generator.generate()
    # with open(DUMP_TRIPS_DATA_FILE, 'w+') as outfile:
    #     json.dump(data, outfile)
    # aggregate()
    # generate_energy_market()
    # disaggregation()
    # file = open(DISAGGREGATION_PATH + ".json", "r")
    # load_aggregated_decisions(file)


@contextmanager
def tmp_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        shutil.rmtree(path)
        os.mkdir(path)
    yield path
    pass


def generate_decision_for_node(date: datetime.date, node: Node):
    path = get_path(date, node)
    with tmp_dir(path) as path:
        data = get_trip_data(
            start_date=datetime.combine(date, time(hour=0, minute=0, tzinfo=UTC)),
            end_date=datetime.combine(date, time(hour=DEADLINE_HOUR_TO_SEND_SCHEDULE, minute=0, tzinfo=UTC)),
            node=node
        )
        with open(os.path.join(path, DUMP_TRIPS_NAME), "w+") as outfile:
            json.dump(data, outfile)
        aggregate(path)
        generate_energy_market(path)
        disaggregation(path)
        with open(os.path.join(path, os.path.join(path, DISAGGREGATION_NAME+".json")), "r") as file:
            data = json.load(file)
            load_aggregated_decisions(date, node, data)


def get_path(date: datetime.date, node: Node):
    name_of_dir = f"{node.name}_{date.strftime('%Y_%m_%d')}"
    return os.path.join(TMP_DATA_DIR, name_of_dir)


def load_aggregated_decisions(date: datetime, node: Node, data):
    decision_data = data["disaggregationResultEntries"][0]
    node_decision, point_schedule_decisions = AggregatorNodeDecisionSchema(unknown=EXCLUDE).load(decision_data)
    decision, created = AggregatorDecision.objects.get_or_create(decision_date=date, defaults={'receive_date': datetime.now()})
    node_decision.decision = decision
    node_decision.node = node
    node_decision.save()
    for point_schedule_decision in point_schedule_decisions:
        point_schedule_decision.decision = node_decision
        point_schedule_decision.save()
