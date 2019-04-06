from django.db import models
from django.contrib.auth.models import User


class ElectricVehicle(models.Model):
    max_battery_capacity = models.IntegerField()
    min_battery_capacity = models.IntegerField()
    max_charging_power = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Node(models.Model):
    address = models.CharField(max_length=200)


class Localization(models.Model):
    address = models.CharField(max_length=200)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)


class Bid(models.Model):
    HOME_HOME = 'hh'
    HOME_WORK_HOME = 'hwh'
    TYPES = (
        (HOME_HOME, 'home-home'),
        (HOME_WORK_HOME, 'home-work-home'),
    )
    date = models.DateTimeField(auto_now=True)
    mode = models.CharField(max_length=3, choices=TYPES)
    electric_vehicle = models.ForeignKey(ElectricVehicle, on_delete=models.CASCADE)


class ChargingLocalization(models.Model):
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    charge_percent = models.DecimalField(max_digits=5, decimal_places=2)
    expected_charge_percent = models.DecimalField(max_digits=5, decimal_places=2)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="charging_localizations")
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE)
