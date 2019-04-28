import datetime
import json

from apps.aggregator_integration.loader import AggregatorDecisionSchema


def load_aggregated_decisions(file):
    today = datetime.datetime.now()
    data = json.load(file)
    decision, charging_localization_decisions = AggregatorDecisionSchema().load(data).data
    decision.decision_date = today.date()
    decision.receive_date = today
    decision.save()
    for charging_localization_decision in charging_localization_decisions:
        charging_localization_decision.decision = decision
        charging_localization_decision.save()
