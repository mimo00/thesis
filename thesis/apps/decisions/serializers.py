from rest_framework import serializers

from apps.decisions.models import PointScheduleDecision
from apps.schedules.serializers import PointScheduleSerializer


class ChargingLocalizationDecisionSerializer(serializers.ModelSerializer):
    point_schedule = PointScheduleSerializer()

    class Meta:
        model = PointScheduleDecision
        fields = ("point_schedule", "start_time", "end_time", "coverage")
