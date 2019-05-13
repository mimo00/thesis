import datetime
from random import randint, randrange, choices

from django.contrib.auth import get_user_model
from faker import Faker
from freezegun import freeze_time
from pytz import UTC

from apps.schedules.models import Node, ChargingPoint, ElectricVehicle, Schedule, PointSchedule


class DemoGenerator:
    def generate(self):
        raise NotImplementedError


class UserDemo(DemoGenerator):
    def generate(self):
        User = get_user_model()
        User.objects.create_superuser("root", "root@root.com", "root")
        names = ["wilder", "joshua", "parker", "ortiz", "kownacki"]
        for name in names:
            user = User.objects.create_user(name, name + "@gmail.com", name)
            for _ in range(3):
                ElectricVehicle.objects.create(
                    max_charging_power=randrange(10, 30), user=user,
                    min_battery_capacity=randrange(5, 10), max_battery_capacity=randrange(15, 20)
                )
                ElectricVehicle.objects.create(
                    max_charging_power=randrange(10, 30), user=user,
                    min_battery_capacity=randrange(5, 10), max_battery_capacity=randrange(15, 20)
                )


class ChargingPointDemo(DemoGenerator):
    NUMBER_OF_NODES = 5
    NUMBER_OF_pointS_FOR_NODE = 2

    def generate(self):
        myFactory = Faker()
        for _ in range(self.NUMBER_OF_NODES):
            node = Node.objects.create(name=myFactory.state())
            for _ in range(self.NUMBER_OF_pointS_FOR_NODE):
                ChargingPoint.objects.create(address=myFactory.address(), node=node)


class FetchingSchedulesDemo(DemoGenerator):
    NUMBERS_OF_DAYS_FOR_SCHEDULES = 5

    def generate(self):
        electric_vehicles = ElectricVehicle.objects.all()
        date_ = datetime.datetime.now(tz=UTC)
        DAY = datetime.timedelta(days=1)
        for _ in range(self.NUMBERS_OF_DAYS_FOR_SCHEDULES):
            for electric_vehicle in electric_vehicles:
                self.generate_schedule(date_, electric_vehicle)
            date_ = date_ - DAY

    def generate_schedule(self, date, ev):
        points = ChargingPoint.objects.all()
        home, work = choices(points, k=2)
        times = self.generate_times(date) #list of 3 dates
        with freeze_time(date):
            schedule = Schedule.objects.create(mode=Schedule.HOME_WORK_HOME, electric_vehicle=ev)
        PointSchedule.objects.create(arrival_time=date.replace(hour=0, minute=0), departure_time=times[0],
                                     charge_percent=50.00, expected_charge_percent=70.00, schedule=schedule, point=home)
        PointSchedule.objects.create(arrival_time=date.replace(hour=8, minute=0), departure_time=times[1], charge_percent=50.00,
                                     expected_charge_percent=60.00, schedule=schedule, point=work)
        PointSchedule.objects.create(arrival_time=date.replace(hour=18, minute=0), departure_time=times[2], charge_percent=30.00,
                                     expected_charge_percent=40.00, schedule=schedule, point=home)

    def generate_times(self, date):
        t1 = date.replace(hour=7, minute=randint(0, 59))
        t2 = date.replace(hour=15, minute=randint(0, 59))
        t3 = date.replace(hour=23, minute=randint(0, 59))
        return [t1, t2, t3]


demos = [UserDemo, ChargingPointDemo, FetchingSchedulesDemo]


def run():
    for demo_cls in demos:
        demo_cls().generate()
