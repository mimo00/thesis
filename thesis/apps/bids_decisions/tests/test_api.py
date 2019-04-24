from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from freezegun import freeze_time
from pytz import UTC
from rest_framework import status

from apps.bids_decisions.factories import BidDecisionFactory, ChargingLocalizationDecisionFactory, \
    AggregatorDecisionFactory
from apps.fetching_bids.factories import ElectricVehicleFactory

test_date = datetime(year=2019, month=4, day=15, hour=16, minute=30, tzinfo=UTC)


@pytest.mark.django_db
class TestBidDecisionView:
    def test_getting_list_of_decisions(self, auth_api_client):
        e_v = ElectricVehicleFactory(user=auth_api_client.user)
        BidDecisionFactory(decision__decision_date=test_date - timedelta(days=1), bid__electric_vehicle=e_v)
        BidDecisionFactory(decision__decision_date=test_date, bid__electric_vehicle=e_v)
        url = reverse("bid_decisions-list")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": e_v.id})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 2

    def test_getting_filter_by_date(self, auth_api_client):
        e_v = ElectricVehicleFactory(user=auth_api_client.user)
        BidDecisionFactory(decision__decision_date=test_date - timedelta(days=1), bid__electric_vehicle=e_v)
        BidDecisionFactory(decision__decision_date=test_date, bid__electric_vehicle=e_v)
        url = reverse("bid_decisions-list")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": e_v.id, "date": test_date.date()})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1

    def test_getting_bid_decision(self, auth_api_client):
        bid_decision = BidDecisionFactory(decision__decision_date=test_date+timedelta(days=1),
                                          bid__electric_vehicle__user=auth_api_client.user)
        ChargingLocalizationDecisionFactory(bid_decision=bid_decision)
        ChargingLocalizationDecisionFactory(bid_decision=bid_decision)
        url = reverse("bid_decisions-next-day")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": bid_decision.bid.electric_vehicle.id})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data['charging_localization_decisions']) == 2
        assert 'charging_localization' in res.data['charging_localization_decisions'][0]
        assert 'start_time' in res.data['charging_localization_decisions'][0]
        assert 'end_time' in res.data['charging_localization_decisions'][0]
        assert 'coverage' in res.data['charging_localization_decisions'][0]

    def test_getting_bid_decision_for_not_permitted_vehicle(self, auth_api_client):
        bid_decision = BidDecisionFactory(decision__decision_date=test_date+timedelta(days=1))
        url = reverse("bid_decisions-next-day")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": bid_decision.bid.electric_vehicle.id})
        assert res.status_code == status.HTTP_403_FORBIDDEN
        assert res.data["detail"] == f"You are trying to get bid for electric vehicle: {bid_decision.bid.electric_vehicle.id} but it is not assigned for your account"

    def test_getting_bid_decision_while_there_is_no_decision(self, auth_api_client):
        fake_electric_vehicle = 123
        expected_checking_date = datetime(year=2019, month=4, day=16, hour=16, minute=30, tzinfo=UTC)
        url = reverse("bid_decisions-next-day")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": fake_electric_vehicle})
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.data["error"] == f"There is no decision for day {expected_checking_date}"

    def test_getting_bid_decision_while_there_is_no_decision_for_that_electric_vehicle(self, auth_api_client):
        e_v = ElectricVehicleFactory(user=auth_api_client.user)
        AggregatorDecisionFactory(decision_date=test_date+timedelta(days=1))
        url = reverse("bid_decisions-next-day")
        with freeze_time(test_date):
            res = auth_api_client.get(url, {"electric_vehicle": e_v.id})
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.data["error"] == f"There is no bid for electric vehicle {e_v.id}"