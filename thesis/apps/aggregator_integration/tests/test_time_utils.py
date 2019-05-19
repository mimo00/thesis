import datetime

from apps.aggregator_integration.time_utils import get_schedule, get_plugin_schedule, get_indexes_ranges, \
    get_time_ranges


def test_getting_schedule():
    start_hour = 2
    end_hour = 5
    result = get_schedule(start_hour, end_hour)
    assert result == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_getting_plugin_schedule():
    date_ranges = [
        (datetime.time(hour=0, minute=10), datetime.time(hour=7, minute=30)),
        (datetime.time(hour=9, minute=0), datetime.time(hour=16, minute=30))
    ]
    plugin_schedule = get_plugin_schedule(date_ranges)
    assert plugin_schedule == [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]


def test_getting_time_ranges():
    schedule = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]
    result = get_time_ranges(schedule)
    assert result == [
        (datetime.time(hour=0), datetime.time(hour=7)),
        (datetime.time(hour=10), datetime.time(hour=16)),
        (datetime.time(hour=22), datetime.time(hour=23)),
    ]


def test_getting_indexes_ranges():
    schedule = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]
    result = get_indexes_ranges(schedule)
    assert result == [(0, 7), (10, 16), (22, 23)]
