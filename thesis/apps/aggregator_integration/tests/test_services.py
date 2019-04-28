from datetime import datetime

import pytest
from pytz import UTC

from apps.aggregator_integration.services import load_aggregated_decisions
from apps.fetching_bids.factories import ChargingLocalizationFactory


@pytest.mark.django_db
def test_load_aggregated_decisions():
    test_date = datetime(year=2019, month=4, day=15, hour=16, minute=0, tzinfo=UTC)
    ChargingLocalizationFactory(id=1, arrival_time=test_date)
    ChargingLocalizationFactory(id=2, arrival_time=test_date)
    test_file_name = open("./apps/aggregator_integration/tests/test_aggregated.txt", "r")
    load_aggregated_decisions(test_file_name)
