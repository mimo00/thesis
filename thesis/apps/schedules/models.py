from django.db import models
from django.contrib.auth.models import User


class ElectricVehicle(models.Model):
    max_battery_capacity = models.IntegerField()
    min_battery_capacity = models.IntegerField()
    max_charging_power = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"ElectricVehicle #{self.pk} owner {self.user}"


class Node(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Node #{self.pk} name {self.name}"


class ChargingPoint(models.Model):
    address = models.CharField(max_length=200)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)


class Schedule(models.Model):
    HOME_HOME = 'hh'
    HOME_WORK_HOME = 'hwh'
    TYPES = (
        (HOME_HOME, 'home-home'),
        (HOME_WORK_HOME, 'home-work-home'),
    )
    date = models.DateTimeField(auto_now=True)
    mode = models.CharField(max_length=3, choices=TYPES)
    charge_percent = models.IntegerField()
    trip_percent = models.IntegerField()
    electric_vehicle = models.ForeignKey(ElectricVehicle, on_delete=models.CASCADE)

    def __str__(self):
        return f"Schedule #{self.pk} mode {self.mode}"


class PointSchedule(models.Model):
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="point_schedules")
    point = models.ForeignKey(ChargingPoint, on_delete=models.CASCADE)

    def __str__(self):
        return f"Schedule #{self.pk} schedule {self.schedule_id}"
