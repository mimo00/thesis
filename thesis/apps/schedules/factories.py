from datetime import datetime

import factory
from django.contrib.auth.models import User

from apps.schedules import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.Faker('email')
    is_staff = False


class NodeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Node


class ChargingPointFactory(factory.DjangoModelFactory):
    node = factory.SubFactory(NodeFactory)

    class Meta:
        model = models.ChargingPoint


class ElectricVehicleFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.ElectricVehicle

    max_battery_capacity = 30
    min_battery_capacity = 50
    max_charging_power = 10


class ScheduleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Schedule

    electric_vehicle = factory.SubFactory(ElectricVehicleFactory)
    mode = models.Schedule.HOME_HOME


class PointScheduleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PointSchedule

    arrival_time = datetime(year=2019, month=7, day=24, hour=6, minute=30)
    departure_time = datetime(year=2019, month=7, day=24, hour=6, minute=30)
    charge_percent = 32.58
    expected_charge_percent = 99.99
    schedule = factory.SubFactory(ScheduleFactory)
    point = factory.SubFactory(ChargingPointFactory)

