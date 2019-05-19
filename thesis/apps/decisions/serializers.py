from rest_framework import serializers

from apps.decisions.models import ScheduleDecision, DateRangeDecision


class DateRangeDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateRangeDecision
        fields = ("start_time", "end_time", )


class SchedulesDecisionSerializer(serializers.ModelSerializer):
    schedule_decision_date_ranges = DateRangeDecisionSerializer(many=True)

    class Meta:
        model = ScheduleDecision
        fields = ("coverage", "schedule_decision_date_ranges")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["schedule_decision_date_ranges"] = sorted(data["schedule_decision_date_ranges"], key=lambda x: x["start_time"])
        return data
