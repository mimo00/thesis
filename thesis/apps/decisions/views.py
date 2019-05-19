from datetime import datetime, timedelta

from dateutil.tz import UTC
from rest_framework import mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.decisions import filters
from apps.decisions.models import ScheduleDecision, AggregatorDecision
from apps.decisions.serializers import SchedulesDecisionSerializer
from apps.schedules.models import ElectricVehicle


class SchedulesDecisionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = ScheduleDecision.objects.all()
    serializer_class = SchedulesDecisionSerializer
    filterset_class = filters.ChargingSchedulesDecisionFilter

    def get_queryset(self):
        return super().get_queryset().filter(schedule__electric_vehicle=self.get_electric_vehicle().id)

    @action(detail=False)
    def next_day(self, request):
        try:
            next_day = datetime.now(tz=UTC) + timedelta(days=1)
            aggregator_decision = AggregatorDecision.objects.get(decision_date=next_day)
            schedule_decision = ScheduleDecision.objects.get(
                schedule__electric_vehicle=self.get_electric_vehicle().id,
                group_decision__decision=aggregator_decision)
            serializer = self.get_serializer(schedule_decision)
            return Response(serializer.data)
        except AggregatorDecision.DoesNotExist:
            return Response({"error": f"There is no decision for day {next_day}"}, status=status.HTTP_404_NOT_FOUND)

    def get_electric_vehicle(self):
        electric_vehicle_id = self.request.query_params.get('electric_vehicle', None)
        if not electric_vehicle_id:
            raise serializers.ValidationError("You need to specify electric_vehicle id.")
        electric_vehicle = ElectricVehicle.objects.get(id=electric_vehicle_id)
        if not electric_vehicle.user == self.request.user:
            error = f"You are trying to get schedule for electric vehicle: {electric_vehicle_id} but it is not assigned for your account"
            raise PermissionDenied(detail=error)
        return electric_vehicle



