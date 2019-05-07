import datetime
from random import randint, randrange, choices

from django.contrib.auth import get_user_model
from faker import Faker
from freezegun import freeze_time
from pytz import UTC

from apps.fetching_bids.models import Node, Localization, ElectricVehicle, Bid, ChargingLocalization


class DemoGenerator:
    def generate(self):
        raise NotImplementedError


class UserDemo(DemoGenerator):
    def generate(self):
        User = get_user_model()
        User.objects.create_superuser("root", "root@root.com", "root")
        self.generate_users()

    def generate_users(self):
        names = ["wilder", "joshua", "parker", "ortiz", "kownacki"]
        User = get_user_model()
        for name in names:
            user = User.objects.create_user(name, name + "@gmail.com", name)
            ElectricVehicle.objects.create(
                max_charging_power=randrange(10, 30, 1), user=user,
                min_battery_capacity=randrange(10, 40, 5), max_battery_capacity=randrange(50, 150, 5)
            )


class LocalizationDemo(DemoGenerator):
    NUMBER_OF_NODES = 5
    NUMBER_OF_LOCALIZATIONS_FOR_NODE = 2

    def generate(self):
        myFactory = Faker()
        for _ in range(self.NUMBER_OF_NODES):
            node = Node.objects.create(address=myFactory.state())
            for _ in range(self.NUMBER_OF_LOCALIZATIONS_FOR_NODE):
                Localization.objects.create(address=myFactory.address(), node=node)


class FetchingBidsDemo(DemoGenerator):
    NUMBERS_OF_DAYS_FOR_BIDS = 5

    def generate(self):
        electric_vehicles = ElectricVehicle.objects.all()
        date_ = datetime.datetime.now(tz=UTC)
        DAY = datetime.timedelta(days=1)
        for _ in range(self.NUMBERS_OF_DAYS_FOR_BIDS):
            for electric_vehicle in electric_vehicles:
                self.generate_bid(date_, electric_vehicle)
            date_ = date_ - DAY

    def generate_bid(self, date, ev):
        localizations = Localization.objects.all()
        home, work = choices(localizations, k=2)
        times = self.generate_times(date) #list of 6 dates
        with freeze_time(date):
            bid = Bid.objects.create(mode=Bid.HOME_WORK_HOME, electric_vehicle=ev)
        ChargingLocalization.objects.create(arrival_time=times[0], departure_time=times[1], charge_percent=50.00,
                                            expected_charge_percent=70.30, bid=bid, localization=home)
        ChargingLocalization.objects.create(arrival_time=times[2], departure_time=times[3], charge_percent=20.00,
                                            expected_charge_percent=90.00, bid=bid, localization=work)
        ChargingLocalization.objects.create(arrival_time=times[4], departure_time=times[5], charge_percent=20.00,
                                            expected_charge_percent=100.00, bid=bid, localization=home)

    def generate_times(self, date):
        times = []
        for hour in self.generate_hours():
            times.append(date.replace(hour=hour, minute=randint(0, 59)))
        return times

    def generate_hours(self):
        hours = []
        start_index = 0
        for i in range(6):
            hours.append(randint(start_index, start_index+3))
            start_index += 4
        return hours


demos = [UserDemo, LocalizationDemo, FetchingBidsDemo]


def run():
    for demo_cls in demos:
        demo_cls().generate()
