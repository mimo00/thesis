import datetime

from django.shortcuts import render, redirect
from django.views import View
from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet

# from apps.aggregator_integration.services import generate_decision
from apps.schedules.forms import TriggerAggregationForm
from apps.schedules.models import Schedule
from apps.schedules.serializers import ScheduleSerializer


class ScheduleViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ScheduleSerializer

    def perform_create(self, serializer):
        if not serializer.validated_data['electric_vehicle'].user == self.request.user:
            raise PermissionDenied(detail="You are trying to send schedule for not your vehicle.")
        super().perform_create(serializer)


def auction_detail(request):
    number_of_today_schedules = Schedule.objects.filter(date__date=datetime.datetime.now().date()).count()
    return render(request, 'fetching/detail.html',
                  {'number_of_today_schedules': number_of_today_schedules})



class TriggerAggregationView(View):
    def get(self, request):
        form = TriggerAggregationForm()
        return render(request, 'aggregation/aggregation.html', {'form': form})
