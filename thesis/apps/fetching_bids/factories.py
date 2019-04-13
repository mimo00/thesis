import factory
from django.contrib.auth.models import User

from apps.fetching_bids import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = "Olga"
    email = "oldzilla@gmail.com"
    is_staff = False


class NodeFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Node


class LocalizationFactory(factory.DjangoModelFactory):
    node = factory.SubFactory(NodeFactory)

    class Meta:
        model = models.Localization


class ElectricVehicleFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.ElectricVehicle

    max_battery_capacity = 30
    min_battery_capacity = 50
    max_charging_power = 10
