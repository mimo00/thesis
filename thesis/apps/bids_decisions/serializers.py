from rest_framework import serializers

from apps.bids_decisions.models import ChargingLocalizationDecision
from apps.fetching_bids.serializers import ChargingLocalizationSerializer


class ChargingLocalizationDecisionSerializer(serializers.ModelSerializer):
    charging_localization = ChargingLocalizationSerializer()

    class Meta:
        model = ChargingLocalizationDecision
        fields = ("charging_localization", "start_time", "end_time", "coverage")
