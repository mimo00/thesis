import datetime
from dataclasses import dataclass
from typing import List

from aggregator.settings import DEADLINE_HOUR_TO_SEND_SCHEDULE

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
