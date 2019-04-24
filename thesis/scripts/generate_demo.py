import datetime

from django.contrib.auth import get_user_model
from pytz import UTC

from apps.bids_decisions.models import AggregatorDecision, BidDecision, ChargingLocalizationDecision
from apps.fetching_bids.models import Node, Localization, ElectricVehicle, Bid, ChargingLocalization


class DemoGenerator:
    def generate(self):
        raise NotImplementedError


class UserDemo(DemoGenerator):
    def generate(self):
        User = get_user_model()
        User.objects.create_superuser("root", "root@root.com", "root")
        deontay_wilder = User.objects.create_user("wilder", "wilder@gmail.com", "wilder")
        node1 = Node.objects.create(address="Wall Street 5")
        node2 = Node.objects.create(address="Beverly Hills 17")
        Localization.objects.create(id=1, address="deontay_wilders_home", node=node1)
        Localization.objects.create(id=2, address="deontay_wilders_work", node=node2)
        ElectricVehicle.objects.create(id=1, max_charging_power=100, min_battery_capacity=30, max_battery_capacity=78, user=deontay_wilder)


test_date = datetime.datetime.now(tz=UTC)
DAY = datetime.timedelta(days=1)
previous_day = test_date-DAY


class FetchingBidsDemo(DemoGenerator):
    def generate(self):
        ev = ElectricVehicle.objects.get(id=1)
        bid = Bid.objects.create(id=1, date=previous_day-DAY, mode=Bid.HOME_WORK_HOME, electric_vehicle=ev)
        home = Localization.objects.get(id=1)
        work = Localization.objects.get(id=2)
        charging_localization1 = ChargingLocalization.objects.create(
            arrival_time=previous_day.replace(hour=0, minute=0), departure_time=previous_day.replace(hour=7, minute=0),
            charge_percent=50.00, expected_charge_percent=70.30, bid=bid, localization=home)
        charging_localization2 = ChargingLocalization.objects.create(
            arrival_time=previous_day.replace(hour=8, minute=0), departure_time=previous_day.replace(hour=15, minute=0),
            charge_percent=20.00, expected_charge_percent=90.00, bid=bid, localization=work)
        charging_localization3 = ChargingLocalization.objects.create(
            arrival_time=previous_day.replace(hour=18, minute=0), departure_time=previous_day.replace(hour=23, minute=59),
            charge_percent=20.00, expected_charge_percent=100.00, bid=bid, localization=home)
        decision = AggregatorDecision.objects.create(
            decision_date=previous_day.date(), receive_date=previous_day.replace(hour=23, minute=0), decision=True)
        bid_decision = BidDecision.objects.create(decision=decision, bid=bid)
        ChargingLocalizationDecision.objects.create(
            bid_decision=bid_decision, charging_localization=charging_localization1, coverage=35.00,
            start_time=previous_day.replace(hour=3, minute=0), end_time=previous_day.replace(hour=7, minute=0))
        ChargingLocalizationDecision.objects.create(
            bid_decision=bid_decision, charging_localization=charging_localization2, coverage=50.00,
            start_time=previous_day.replace(hour=8, minute=0), end_time=previous_day.replace(hour=11, minute=0))
        ChargingLocalizationDecision.objects.create(
            bid_decision=bid_decision, charging_localization=charging_localization3, coverage=20.00,
            start_time=previous_day.replace(hour=20, minute=0), end_time=previous_day.replace(hour=22, minute=0))


demos = [UserDemo, FetchingBidsDemo, ]


def run():
    for demo_cls in demos:
        demo_cls().generate()
