import datetime

class Request:
    ...

class Throttler:
    def __init__(self, *, per_second: int):
        self.per_second = per_second
        self.requests_this_period = 0
        self.start_of_period = None

    def check(self, request: Request):
        now = datetime.datetime.now()

        if self.start_of_period is None:
            self.start_of_period = now

        if now - self.start_of_period >= datetime.timedelta(seconds=1):
            print(f"{now.second=} is at least one second past {self.start_of_period=}")
            self.start_of_period = now
            self.requests_this_period = 0
            print(f"... so set {self.start_of_period=} and {self.requests_this_period=}")

        if self.requests_this_period == self.per_second:
            print(f"{self.requests_this_period=} == {self.per_second=}, so returning False")
            return False

        print(f"{self.requests_this_period=} != {self.per_second=}, so returning True, and bumping the former")

        self.requests_this_period += 1

        return True

    def __repr__(self):
        return repr(vars(self))
