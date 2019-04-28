import django_filters
from django_filters.rest_framework import FilterSet


class ChargingLocalizationDecisionFilter(FilterSet):
    date = django_filters.DateFilter(field_name="decision__decision_date", help_text="Date of decision.")

