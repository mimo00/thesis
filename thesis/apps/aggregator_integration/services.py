import datetime
import json

from marshmallow import EXCLUDE

from apps.aggregator_integration.aggregator_commands import aggregate, generate_energy_market, disaggregation
from apps.aggregator_integration.generator import AggregatorInputGenerator
from apps.aggregator_integration.loader import AggregatorDecisionSchema
from apps.bids_decisions.models import AggregatorDecision
from evs_bids.settings import DUMP_TRIPS_DATA_FILE, DISAGGREGATION_PATH


def load_aggregated_decisions(file):
    today = datetime.datetime.now()
    data = json.load(file)
    decision_data = data["disaggregationResultEntries"][0]
    decision, charging_localization_decisions = AggregatorDecisionSchema(unknown=EXCLUDE).load(decision_data)
    decision.decision_date = today.date()
    decision.receive_date = today
    decision.save()
    for charging_localization_decision in charging_localization_decisions:
        charging_localization_decision.decision = decision
        charging_localization_decision.save()


def generate_decision():
    today = datetime.datetime.now()
    a_d = AggregatorDecision.objects.filter(decision_date=today.date())
    if a_d.exists():
        a_d.delete()
    generator = AggregatorInputGenerator(date=today)
    data = generator.generate()
    with open(DUMP_TRIPS_DATA_FILE, 'w+') as outfile:
        json.dump(data, outfile)
    aggregate()
    generate_energy_market()
    disaggregation()
    file = open(DISAGGREGATION_PATH + ".json", "r")
    load_aggregated_decisions(file)
