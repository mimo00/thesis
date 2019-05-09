from rest_framework import serializers
from apps.schedules.models import Schedule, PointSchedule


class PointScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointSchedule
        fields = ("departure_time", "arrival_time", "point", "expected_charge_percent", "charge_percent")


class ScheduleSerializer(serializers.ModelSerializer):
    point_schedules = PointScheduleSerializer(many=True, allow_null=False)

    class Meta:
        model = Schedule
        fields = ("mode", "point_schedules", "electric_vehicle")

    def validate(self, data):
        if data['mode'] == Schedule.HOME_HOME and len(data['point_schedules']) != 2:
            raise serializers.ValidationError("In home to home mode specify 2 points")
        if data['mode'] == Schedule.HOME_WORK_HOME and len(data['point_schedules']) != 3:
            raise serializers.ValidationError("In home to home mode specify 3 points")
        return data

    def create(self, validated_data):
        point_schedules_data = validated_data.pop('point_schedules')
        schedule = Schedule.objects.create(**validated_data)
        for point_schedule in point_schedules_data:
            PointSchedule.objects.create(**point_schedule, schedule=schedule)
        return schedule

