from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from apps.schedules.factories import ElectricVehicleFactory, ChargingPointFactory, UserFactory


@pytest.mark.django_db
class TestScheduleViewSet:
    def test_post_proper_schedule(self, auth_api_client):
        ev = ElectricVehicleFactory(user=auth_api_client.user)
        home = ChargingPointFactory()
        data = {
            "electric_vehicle": ev.id,
            "mode": "hh",
            "point_schedules": [
                {
                    "point": home.id,
                    "arrival_time": datetime(2019, 3, 10, 8, 30, 0),
                    "departure_time": datetime(2019, 3, 10, 8, 30, 0),
                    "charge_percent": 10,
                    "expected_charge_percent": 60
                },
                {
                    "point": home.id,
                    "arrival_time": datetime(2019, 3, 10, 8, 30, 0),
                    "departure_time": datetime(2019, 3, 10, 8, 30, 0),
                    "charge_percent": 5,
                    "expected_charge_percent": 100
                }
            ]
        }
        url = reverse("charging-schedules-list")
        res = auth_api_client.post(url, data, format="json")
        assert res.status_code == status.HTTP_201_CREATED

    def test_unauthorized_client_can_not_post_schedule(self, api_client):
        ElectricVehicleFactory()
        data = {}
        url = reverse("charging-schedules-list")
        res = api_client.post(url, data, format="json")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_can_not_create_schedule_for_not_his_vehicle(self, auth_api_client):
        owner = UserFactory(username="test")
        ev = ElectricVehicleFactory(user=owner)
        home = ChargingPointFactory()
        data = {
            "electric_vehicle": ev.id,
            "mode": "hh",
            "point_schedules": [
                {
                    "point": home.id,
                    "arrival_time": datetime(2019, 3, 10, 8, 30, 0),
                    "departure_time": datetime(2019, 3, 10, 8, 30, 0),
                    "charge_percent": 10,
                    "expected_charge_percent": 60
                },
                {
                    "point": home.id,
                    "arrival_time": datetime(2019, 3, 10, 8, 30, 0),
                    "departure_time": datetime(2019, 3, 10, 8, 30, 0),
                    "charge_percent": 5,
                    "expected_charge_percent": 100
                }
            ]
        }
        url = reverse("charging-schedules-list")
        res = auth_api_client.post(url, data, format="json")
        assert res.status_code == status.HTTP_403_FORBIDDEN
        assert res.data["detail"] == "You are trying to send schedule for not your vehicle."

    def test_wrong_number_of_point(self, auth_api_client):
        ev = ElectricVehicleFactory(user=auth_api_client.user)
        home = ChargingPointFactory()
        data = {
            "electric_vehicle": ev.id,
            "mode": "hh",
            "point_schedules": [
                {
                    "point": home.id,
                    "arrival_time": datetime(2019, 3, 10, 8, 30, 0),
                    "departure_time": datetime(2019, 3, 10, 8, 30, 0),
                    "charge_percent": 10,
                    "expected_charge_percent": 60
                }
            ]
        }
        url = reverse("charging-schedules-list")
        res = auth_api_client.post(url, data, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data['non_field_errors'] == ["In home to home mode specify 2 points"]
