from rest_framework import serializers

from apps.bids_decisions.models import BidDecision, ChargingLocalizationDecision
from apps.fetching_bids.serializers import ChargingLocalizationSerializer


class ChargingLocalizationDecisionSerializer(serializers.ModelSerializer):
    charging_localization = ChargingLocalizationSerializer()

    class Meta:
        model = ChargingLocalizationDecision
        fields = ("charging_localization", "start_time", "end_time", "coverage")


class BidDecisionSerializer(serializers.ModelSerializer):
    charging_localization_decisions = ChargingLocalizationDecisionSerializer(many=True, allow_null=False)

    class Meta:
        model = BidDecision
        fields = ("charging_localization_decisions", )
