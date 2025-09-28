from freezegun import freeze_time

from throttler import Request, Throttler


def test_basics() -> None:
    throttler = Throttler(per_second=3)

    request = Request()

    with freeze_time("2012-01-14T00:00:00Z"):
        for _ in range(3):
            assert throttler.check(request)
        assert not throttler.check(request)

    with freeze_time("2012-01-14T00:00:01Z"):
        for _ in range(3):
            assert throttler.check(request)
        assert not throttler.check(request)
