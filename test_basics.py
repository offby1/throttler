from freezegun import freeze_time

from throttler import Request, Throttler


def test_basics() -> None:
    throttler = Throttler(per_period=3)

    request = Request()

    with freeze_time("2012-01-14T00:00:00Z"):
        for _ in range(3):
            assert throttler.check(request)
        assert not throttler.check(request)

    with freeze_time("2012-01-14T00:00:01Z"):
        for _ in range(3):
            assert throttler.check(request)
        assert not throttler.check(request)


def test_longer_period() -> None:
    throttler = Throttler(per_period=10, period_seconds=60)

    request = Request()

    with freeze_time("2012-01-14T00:00:00Z"):
        for _ in range(10):
            assert throttler.check(request)
        assert not throttler.check(request)

    with freeze_time("2012-01-14T00:00:01Z"):
        assert not throttler.check(request)

    with freeze_time("2012-01-14T00:01:00Z"):
        for _ in range(10):
            assert throttler.check(request)
        assert not throttler.check(request)
