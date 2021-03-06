from datetime import datetime

import pytest
from freezegun import freeze_time

from apps.aggregator_integration.loader import AggregatorGroupDecisionSchema, OfferSchema
from apps.decisions.factories import AggregatorGroupDecisionFactory
from apps.schedules.factories import ElectricVehicleFactory, ScheduleFactory


@pytest.mark.django_db
class TestLoading:
    def test_loading_data(self):
        ev1 = ElectricVehicleFactory()
        ev2 = ElectricVehicleFactory()
        with freeze_time(datetime.now()):
            ScheduleFactory(electric_vehicle=ev1)
            ScheduleFactory(electric_vehicle=ev2)
        data = {
            "disaggregatedTripsData": [{
                "data": {
                    'id': ev1.id,
                    'plugInSchedule': {
                        'schedule': [],
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
                "chargeHours": [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
            }, {
                "data": {
                    'id': ev2.id,
                    'plugInSchedule': {
                        'schedule': [],
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
        decision, schedule_decisions = AggregatorGroupDecisionSchema().load(data)
        assert decision.energy_coverage == 10.34
        assert decision.hour_coverage == 14.23
        assert decision.energy_loss == 2.45
        assert len(schedule_decisions) == 2
        assert len(schedule_decisions[0][1]) == 2
        assert len(schedule_decisions[1][1]) == 1


@pytest.mark.django_db
class TestOfferLoading:
    def test_load_offer(self):
        group_decision = AggregatorGroupDecisionFactory()
        data = {
            "energyDemands": [
                0.0,
                388.5,
                388.5,
                388.5,
                388.5,
                388.5,
                388.5,
                388.5,
                0.0,
                388.5,
                388.5,
                388.5,
                388.5,
                388.5,
                388.5,
                388.5,
                0.0,
                0.0,
                0.0,
                388.5,
                388.5,
                388.5,
                388.5,
                388.5,
            ],
            "totalEnergyDemand": 7260.0,
            "totalNumberOfSchemes": 121,
        }
        offer = OfferSchema().load({**data, "group_decision": group_decision.id})
        assert offer.number_of_schemas == 121
        assert offer.total_energy == 7260
        assert len(offer.hour_offers.all()) == 24
