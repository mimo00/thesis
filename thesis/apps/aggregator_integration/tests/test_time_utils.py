from apps.aggregator_integration.time_utils import get_schedule


def test_getting_schedule():
    start_hour = 2
    end_hour = 5
    result = get_schedule(start_hour, end_hour)
    assert result == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
