from freezegun import freeze_time

from throttler import Request, Throttler


def test_basics() -> None:
    throttler = Throttler(per_period=3)

    request = Request(origin="whatever")

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

    request = Request(origin="whatever")

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


def test_distinguishes_clients() -> None:
    throttler = Throttler(per_period=3)

    freds_request = Request(origin="fred")
    bobs_request = Request(origin="bob")

    with freeze_time("2012-01-14T00:00:00Z"):
        for _ in range(3):
            assert throttler.check(freds_request)
        assert not throttler.check(freds_request)

        for _ in range(3):
            assert throttler.check(bobs_request)
        assert not throttler.check(bobs_request)
