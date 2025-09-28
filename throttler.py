import collections
import datetime

Origin = str

class Request:
    def __init__(self, *, origin: Origin):
        self.origin = origin


class Throttler:
    def __init__(self, *, per_period: int, period_seconds: int = 1):
        self.period_seconds = period_seconds
        self.per_period = per_period
        self.requests_this_period_by_origin: dict[Origin, int] = collections.defaultdict(int)
        self.start_of_period = datetime.datetime.min

    def check(self, request: Request) -> bool:
        now = datetime.datetime.now()
        origin = request.origin

        if now - self.start_of_period >= datetime.timedelta(seconds=self.period_seconds):
            print(f"{now.second=} is at least one second past {self.start_of_period=}")
            self.start_of_period = now
            self.requests_this_period_by_origin[origin] = 0
            print(f"... so set {self.start_of_period=} and {self.requests_this_period_by_origin[origin]=}")

        if self.requests_this_period_by_origin[origin] == self.per_period:
            print(f"{self.requests_this_period_by_origin[origin]=} == {self.per_period=}, so returning False")
            return False

        print(
            f"{self.requests_this_period_by_origin[origin]=} != {self.per_period=}, so returning True, and bumping the former"
        )

        self.requests_this_period_by_origin[origin] += 1

        return True

    def __repr__(self) -> str:
        return repr(vars(self))
