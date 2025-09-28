class Request:
    ...

class Throttler:
    def __init__(self, *, per_second: int):
        ...

    def check(self, request: Request):
        return True
