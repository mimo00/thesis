import datetime
from dataclasses import dataclass
from typing import List, Tuple

from aggregator.settings import DEADLINE_HOUR_TO_SEND_SCHEDULE
from apps.decisions.models import DateRangeDecision

ACTIVE_NUM = 1
NOT_ACTIVE_NUM = 0


@dataclass
class IndexRange:
    start: int
    end: int
    is_empty: bool


@dataclass
class DateRange:
    start: datetime
    end: datetime
    is_empty: bool


def get_index_range(schedule: List[int]) -> IndexRange:
    assert len(schedule) == 24, "Schedule length should be 24 !"
    if ACTIVE_NUM in schedule:
        start = schedule.index(ACTIVE_NUM)
        schedule.reverse()
        end = len(schedule) - 1 - schedule.index(ACTIVE_NUM)
        return IndexRange(start=start, end=end, is_empty=False)
    else:
        return IndexRange(start=-1, end=-1, is_empty=True)


def get_date_range(schedule: List[int], date: datetime):
    index_range = get_index_range(schedule)
    if not index_range.is_empty:
        end = index_range.end + 1 if index_range.end < 23 else 23
        start_time = datetime.datetime(
            year=date.year, month=date.month, day=date.day, hour=index_range.start, tzinfo=date.tzinfo)
        end_time = datetime.datetime(
            year=date.year, month=date.month, day=date.day, hour=end, tzinfo=date.tzinfo)
        return DateRange(start=start_time, end=end_time, is_empty=False)
    else:
        return DateRange(start=None, end=None, is_empty=False)


def get_schedule(start_hour, end_hour):
    schedule = []
    for hour in range(24):
        schedule.append(ACTIVE_NUM) if start_hour < hour < end_hour else schedule.append(NOT_ACTIVE_NUM)
    return schedule


def get_date_rage_for_scheduling(date: datetime):
    start_date = date.replace(hour=0, minute=0, second=0)
    end_date = date.replace(hour=DEADLINE_HOUR_TO_SEND_SCHEDULE, minute=0, second=0)
    return DateRange(start=start_date, end=end_date, is_empty=False)


def get_plugin_schedule(date_ranges: List[Tuple[datetime.time, datetime.time]]) -> List[int]:
    date_ranges = sorted(date_ranges, key=lambda x: x[0])
    schedule = []
    for hour in range(24):
        schedule.append(ACTIVE_NUM) if is_in_time_ranges(hour, date_ranges) else schedule.append(NOT_ACTIVE_NUM)
    return schedule


def is_in_time_ranges(hour, date_ranges: List[Tuple[datetime.time, datetime.time]]):
    for date_range in date_ranges:
        if is_in_time_range(hour, date_range):
            return True
    return False


def is_in_time_range(hour, date_range: Tuple[datetime.time, datetime.time]):
    return date_range[0].hour < hour <= date_range[1].hour


def get_time_ranges(plugin_schedule: List[int]) -> List[Tuple[datetime.time, datetime.time]]:
    time_ranges = []
    range_indexes = get_indexes_ranges(plugin_schedule)
    for range_index in range_indexes:
        time_ranges.append((datetime.time(hour=range_index[0]), datetime.time(hour=range_index[1])))
    return time_ranges


def get_indexes_ranges(plugin_schedule: List[int]) -> List[Tuple[int, int]]:
    starting_hours = []
    ending_hours = []
    if plugin_schedule[0] == ACTIVE_NUM:
        starting_hours.append(0)
    if plugin_schedule[-1] == ACTIVE_NUM:
        ending_hours.append(len(plugin_schedule)-1)
    for hour in range(len(plugin_schedule)-1):
        if plugin_schedule[hour] == 0 and plugin_schedule[hour+1] == 1:
            starting_hours.append(hour+1)
        if plugin_schedule[hour] == 1 and plugin_schedule[hour + 1] == 0:
            ending_hours.append(hour)
    return list(zip(sorted(starting_hours), sorted(ending_hours)))
