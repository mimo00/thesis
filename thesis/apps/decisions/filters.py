import django_filters
from django_filters.rest_framework import FilterSet


class ChargingSchedulesDecisionFilter(FilterSet):
    date = django_filters.DateFilter(field_name="group_decision__decision__decision_date", help_text="Date of decision.")

