import datetime
from dataclasses import dataclass
from typing import List


ACTIVE_NUM = 1

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
