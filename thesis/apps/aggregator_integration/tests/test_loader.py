from datetime import datetime

import pytest
from pytz import UTC

from apps.aggregator_integration.loader import AggregatorDecisionSchema
from apps.fetching_bids.factories import ChargingLocalizationFactory, ElectricVehicleFactory


@pytest.mark.django_db
class TestLoading:
    def test_loading_data(self):
        test_arrival_1 = datetime(year=2019, month=4, day=15, hour=17, minute=3, tzinfo=UTC)
        test_departure_1 = datetime(year=2019, month=4, day=15, hour=23, minute=20, tzinfo=UTC)
        test_arrival_2 = datetime(year=2019, month=4, day=15, hour=1, minute=10, tzinfo=UTC)
        test_departure_2 = datetime(year=2019, month=4, day=15, hour=6, minute=20, tzinfo=UTC)
        ev = ElectricVehicleFactory()
        ch_l_1 = ChargingLocalizationFactory(
            arrival_time=test_arrival_1, departure_time=test_departure_1, bid__electric_vehicle=ev)
        ch_l_2 = ChargingLocalizationFactory(
            arrival_time=test_arrival_2, departure_time=test_departure_2, bid__electric_vehicle=ev)
        data = {
            "disaggregatedTripsData": [{
                    "data": {
                        'id': ev.id,
                        'localization': 1,
                        'plugInSchedule': {
                            'schedule': [
                                False, False, False, False, False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, True, True, True, True, True, True],
                        },
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
                        'id': ev.id,
                        'localization': 1,
                        'plugInSchedule': {
                            'schedule': [
                                False, True, True, True, True, True, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False, False, False, False, False
                            ],
                        },
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
            "totalNumberOfSchemes": 2,
            "totalEnergyCoverage": 10.34,
            "totalHourCoverage": 14.23,
            "totalEnergyLoss": 2.45
        }
        decision, charging_localization_decisions = AggregatorDecisionSchema().load(data)
        assert decision.energy_coverage == 10.34
        assert decision.hour_coverage == 14.23
        assert decision.energy_loss == 2.45
        assert len(charging_localization_decisions) == 2
        assert charging_localization_decisions[0].charging_localization == ch_l_1
        assert charging_localization_decisions[0].start_time == None
        assert charging_localization_decisions[1].charging_localization == ch_l_2
        assert charging_localization_decisions[1].start_time == datetime(year=2019, month=4, day=15, hour=3, minute=0, tzinfo=UTC)
        assert charging_localization_decisions[1].end_time == datetime(year=2019, month=4, day=15, hour=6, minute=0, tzinfo=UTC)

