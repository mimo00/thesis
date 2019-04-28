from datetime import datetime

import pytest
from pytz import UTC

from apps.aggregator_integration.loader import AggregatorDecisionSchema
from apps.fetching_bids.factories import ChargingLocalizationFactory


@pytest.mark.django_db
class TestLoading:
    def test_loading_data(self):
        test_date = datetime(year=2019, month=4, day=15, hour=16, minute=0, tzinfo=UTC)
        ch_l_1 = ChargingLocalizationFactory(arrival_time=test_date)
        ch_l_2 = ChargingLocalizationFactory(arrival_time=test_date)
        data = {
            "disaggregatedTripsData": [{
                    "data": {
                        'id': ch_l_1.id,
                        'localization': 1,
                        'plugInSchedule': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        'battery': {
                            'batteryProfile': {
                                'hourPercentageCharge': 10.0,
                                'capacity': 100.0
                            },
                            'inputEnergyLevel': 10.0,
                            'outputEnergyLevel': 99.99
                        }
                    },
                    "coverage": 0.0,
                    "chargeHours": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }, {
                    "data": {
                        'id': ch_l_2.id,
                        'localization': 1,
                        'plugInSchedule': [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        'battery': {
                            'batteryProfile': {
                                'hourPercentageCharge': 10.0,
                                'capacity': 100.0
                            },
                            'inputEnergyLevel': 10.0,
                            'outputEnergyLevel': 99.99
                        }
                    },
                    "coverage": 50.0,
                    "chargeHours": [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                },

            ],
            "totalNumberOfSchemas": 2,
            "totalEnergyCoverage": 10.34,
            "totalHourCoverage": 14.23,
            "totalEnergyLoss": 2.45
        }
        decision, charging_localization_decisions = AggregatorDecisionSchema().load(data).data
        assert decision.energy_coverage == 10.34
        assert decision.hour_coverage == 14.23
        assert decision.energy_loss == 2.45
        assert len(charging_localization_decisions) == 2
        assert charging_localization_decisions[0].charging_localization == ch_l_1
        assert charging_localization_decisions[0].start_time == None
        assert charging_localization_decisions[1].charging_localization == ch_l_2
        assert charging_localization_decisions[1].start_time == datetime(year=2019, month=4, day=15, hour=3, minute=0, tzinfo=UTC)
        assert charging_localization_decisions[1].end_time == datetime(year=2019, month=4, day=15, hour=6, minute=0, tzinfo=UTC)

