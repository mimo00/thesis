from rest_framework import serializers
from apps.fetching_bids.models import Bid, ChargingLocalization


class ChargingLocalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingLocalization
        fields = ("departure_time", "arrival_time", "localization", "expected_charge_percent", "charge_percent")


class BidSerializer(serializers.ModelSerializer):
    charging_localizations = ChargingLocalizationSerializer(many=True, allow_null=False)

    class Meta:
        model = Bid
        fields = ("mode", "charging_localizations", "electric_vehicle")

    def validate(self, data):
        if data['mode'] == Bid.HOME_HOME and len(data['charging_localizations']) != 2:
            raise serializers.ValidationError("In home to home mode specify 2 localizations")
        if data['mode'] == Bid.HOME_WORK_HOME and len(data['charging_localizations']) != 3:
            raise serializers.ValidationError("In home to home mode specify 3 localizations")
        return data

    def create(self, validated_data):
        charging_localizations_data = validated_data.pop('charging_localizations')
        bid = Bid.objects.create(**validated_data)
        for charging_localization in charging_localizations_data:
            ChargingLocalization.objects.create(**charging_localization, bid=bid)
        return bid

