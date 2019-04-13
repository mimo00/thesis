from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet

from apps.fetching_bids.serializers import BidSerializer


class BidViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = BidSerializer

    def perform_create(self, serializer):
        if not serializer.validated_data['electric_vehicle'].user == self.request.user:
            raise PermissionDenied(detail="You are trying to send bid for not your vehicle.")
        super().perform_create(serializer)



