from django.forms import forms, ChoiceField, IntegerField

from apps.aggregator_integration.services import COVERAGE, MINIMUM_ENERGY_OFFER, ALL_TOGETHER, BY_DESTINATIONS


class TriggerAggregationForm(forms.Form):
    method = ChoiceField(choices=[(ALL_TOGETHER, "All together"), (BY_DESTINATIONS, "By destination")])
    minimum_energy_offer = IntegerField(min_value=500, max_value=10000, initial=MINIMUM_ENERGY_OFFER)
    coverage = IntegerField(min_value=1, max_value=100, initial=COVERAGE)
