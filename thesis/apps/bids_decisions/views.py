from datetime import datetime, timedelta

from dateutil.tz import UTC
from rest_framework import mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.bids_decisions import filters
from apps.bids_decisions.models import ChargingLocalizationDecision, AggregatorDecision
from apps.bids_decisions.serializers import ChargingLocalizationDecisionSerializer
from apps.fetching_bids.models import ElectricVehicle


class ChargingLocalizationDecisionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = ChargingLocalizationDecision.objects.all()
    serializer_class = ChargingLocalizationDecisionSerializer
    filterset_class = filters.ChargingLocalizationDecisionFilter

    def get_queryset(self):
        return super().get_queryset().filter(charging_localization__bid__electric_vehicle=self.get_electric_vehicle().id)

    @action(detail=False)
    def next_day(self, request):
        try:
            next_day = datetime.now(tz=UTC) + timedelta(days=1)
            aggregator_decision = AggregatorDecision.objects.get(decision_date=next_day)
            charging_localization_decision = ChargingLocalizationDecision.objects.filter(
                charging_localization__bid__electric_vehicle=self.get_electric_vehicle().id,
                decision=aggregator_decision)
            if len(charging_localization_decision) == 0:
                error = {"error": f"There is no bid for electric vehicle {request.query_params['electric_vehicle']}"}
                return Response(error, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(charging_localization_decision, many=True)
            return Response(serializer.data)
        except AggregatorDecision.DoesNotExist:
            return Response({"error": f"There is no decision for day {next_day}"}, status=status.HTTP_404_NOT_FOUND)

    def get_electric_vehicle(self):
        electric_vehicle_id = self.request.query_params.get('electric_vehicle', None)
        if not electric_vehicle_id:
            raise serializers.ValidationError("You need to specify electric_vehicle id.")
        electric_vehicle = ElectricVehicle.objects.get(id=electric_vehicle_id)
        if not electric_vehicle.user == self.request.user:
            error = f"You are trying to get bid for electric vehicle: {electric_vehicle_id} but it is not assigned for your account"
            raise PermissionDenied(detail=error)
        return electric_vehicle



