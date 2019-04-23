from datetime import datetime, timedelta

from dateutil.tz import UTC
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.bids_decisions import filters
from apps.bids_decisions.models import BidDecision, AggregatorDecision
from apps.bids_decisions.serializers import BidDecisionSerializer
from apps.fetching_bids.models import ElectricVehicle


class BidDecisionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = BidDecision.objects.all()
    serializer_class = BidDecisionSerializer
    filterset_class = filters.BidDecisionFilter

    def get_queryset(self):
        return super().get_queryset().filter(bid__electric_vehicle=self.get_electric_vehicle().id)

    @action(detail=False)
    def next_day(self, request):
        try:
            next_day = datetime.now(tz=UTC) + timedelta(days=1)
            aggregator_decision = AggregatorDecision.objects.get(decision_date=next_day, decision=True)
            bid_decision = BidDecision.objects.get(
                decision=aggregator_decision, bid__electric_vehicle=self.get_electric_vehicle().id)
            serializer = self.get_serializer(bid_decision)
            return Response(serializer.data)
        except AggregatorDecision.DoesNotExist:
            return Response({"error": f"There is no decision for day {next_day}"}, status=status.HTTP_404_NOT_FOUND)
        except BidDecision.DoesNotExist:
            error = {"error": f"There is no bid for electric vehicle {request.query_params['electric_vehicle']}"}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

    def get_electric_vehicle(self):
        electric_vehicle_id = self.request.query_params['electric_vehicle']
        electric_vehicle = ElectricVehicle.objects.get(id=electric_vehicle_id)
        if not electric_vehicle.user == self.request.user:
            error = f"You are trying to get bid for electric vehicle: {electric_vehicle_id} but it is not assigned for your account"
            raise PermissionDenied(detail=error)
        return electric_vehicle



